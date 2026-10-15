#!/usr/bin/env python3
"""Install, verify, or extract the explicitly shared Codex settings."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys

try:
    import tomlkit
except ImportError:
    sys.exit("Missing dependency: install requirements.txt with Python 3.11+ first.")


AGENT_NAMES = ("advisor.toml", "explorer.toml", "worker.toml")
ROLE_FIELDS = (
    "name", "description", "model", "model_reasoning_effort",
    "developer_instructions",
)
SHARED_PATHS = {
    ("model",): str,
    ("model_reasoning_effort",): str,
    ("agents", "max_concurrent_threads_per_session"): int,
    ("agents", "default_subagent_model"): str,
    ("agents", "default_subagent_reasoning_effort"): str,
}


def read_toml(path, *, optional=False):
    if optional and not path.exists():
        return tomlkit.document()
    with path.open(encoding="utf-8", newline="") as stream:
        return tomlkit.parse(stream.read())


def shared_values(document, *, strict):
    values = {}
    for key, value in document.items():
        if key == "agents":
            if not isinstance(value, dict):
                if strict:
                    raise ValueError("Shared agents must be a TOML table")
                continue
            entries = [((key, child), item) for child, item in value.items()]
        else:
            entries = [((key,), value)]
        for path, item in entries:
            expected = SHARED_PATHS.get(path)
            if expected is None:
                if strict:
                    raise ValueError(f"Unknown shared key: {'.'.join(path)}")
                continue
            raw = item.unwrap() if hasattr(item, "unwrap") else item
            if type(raw) is not expected:
                raise ValueError(f"Invalid value type for {'.'.join(path)}")
            values[path] = raw
    return values


def merge_shared(local, values):
    for path, value in values.items():
        table = local
        if len(path) == 2:
            if "agents" not in local:
                local["agents"] = tomlkit.table()
            table = local["agents"]
            if not isinstance(table, dict):
                raise ValueError("Local agents must be a TOML table to merge shared settings")
        table[path[-1]] = value
    return local


def validate_sources(source):
    guidance = source / "AGENTS.md"
    if not guidance.is_file():
        raise ValueError(f"Missing required file: {guidance}")
    for name in AGENT_NAMES:
        path = source / "agents" / name
        role = read_toml(path)
        for field in ROLE_FIELDS:
            if not isinstance(role.get(field), str) or not role[field].strip():
                raise ValueError(f"Missing {field} in {path}")


def verify(repo_root, codex_home):
    """Read back managed files and declared keys without changing either tree."""
    try:
        revision = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", "HEAD"],
            check=True, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        revision = "unknown"
    print(f"Host: {socket.gethostname()}")
    print(f"OS: {platform.system()}")
    print(f"Source repository: {repo_root.resolve()}")
    print(f"Source HEAD revision: {revision}")
    print(f"Codex home: {codex_home.resolve()}")
    print(f"Observed at (UTC): {datetime.now(timezone.utc).isoformat()}")

    problems = []

    def read_bytes(path, label):
        try:
            return path.read_bytes()
        except FileNotFoundError:
            problems.append(f"Missing file: {label}")
        except OSError:
            problems.append(f"Cannot read file: {label}")
        return None

    portable = repo_root / "codex"
    for relative in (Path("AGENTS.md"), *(Path("agents") / name for name in AGENT_NAMES)):
        source = read_bytes(portable / relative, f"codex/{relative.as_posix()}")
        installed = read_bytes(codex_home / relative, relative.as_posix())
        if source is not None and installed is not None and source != installed:
            problems.append(f"File mismatch: {relative.as_posix()}")

    def read_config(path, label):
        content = read_bytes(path, label)
        if content is None:
            return None
        try:
            return tomlkit.parse(content.decode("utf-8"))
        except (UnicodeError, tomlkit.exceptions.ParseError):
            problems.append(f"Invalid TOML: {label}")
            return None

    shared = read_config(portable / "config.shared.toml", "codex/config.shared.toml")
    local = read_config(codex_home / "config.toml", "config.toml")
    if shared is not None:
        try:
            declared = shared_values(shared, strict=True)
        except ValueError as error:
            problems.append(str(error))
        else:
            if local is not None:
                missing = object()
                for path, expected in declared.items():
                    actual = local
                    for key in path:
                        actual = actual.get(key, missing) if isinstance(actual, dict) else missing
                    if actual is missing:
                        problems.append(f"Missing key: config.toml:{'.'.join(path)}")
                    else:
                        actual = actual.unwrap() if hasattr(actual, "unwrap") else actual
                        if type(actual) is not type(expected) or actual != expected:
                            problems.append(f"Key mismatch: config.toml:{'.'.join(path)}")
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print("Verification failed.", file=sys.stderr)
        return False
    print("Verified managed files and declared shared settings.")
    return True


def run(action, repo_root, codex_home):
    if action == "verify":
        return 0 if verify(repo_root, codex_home) else 1
    portable = repo_root / "codex"
    shared_path = portable / "config.shared.toml"
    local_path = codex_home / "config.toml"
    # Validate every input before any destination is changed.
    declared = shared_values(read_toml(shared_path), strict=True)
    local = read_toml(local_path, optional=action == "install")
    source, target = (portable, codex_home) if action == "install" else (codex_home, portable)
    validate_sources(source)
    if action == "install":
        config_text = tomlkit.dumps(merge_shared(local, declared))
        config_target = local_path
    else:
        extracted = merge_shared(tomlkit.document(), shared_values(local, strict=False))
        config_text = tomlkit.dumps(extracted)
        config_target = shared_path

    (target / "agents").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / "AGENTS.md", target / "AGENTS.md")
    for name in AGENT_NAMES:
        shutil.copyfile(source / "agents" / name, target / "agents" / name)
    with config_target.open("w", encoding="utf-8", newline="") as stream:
        stream.write(config_text)
    if action == "install":
        state_path = codex_home / ".portable-config-agent-files"
        if state_path.is_file():
            for name in state_path.read_text(encoding="utf-8").splitlines():
                if not name or "/" in name or "\\" in name or name in (".", ".."):
                    continue
                previous = target / "agents" / name
                if name not in AGENT_NAMES and previous.is_file():
                    previous.unlink()
        state_path.write_text("\n".join(AGENT_NAMES) + "\n", encoding="utf-8")
        print(f"Installed AGENTS.md, {len(AGENT_NAMES)} managed agents, and declared shared settings into {target}")
        print("Unmanaged config settings and local agents were retained.")
        return 0 if verify(repo_root, codex_home) else 1
    else:
        print(f"Synced AGENTS.md, {len(AGENT_NAMES)} managed agents, and allowed shared settings into {target}")
        print("Review git diff before committing. Local config.toml was not changed.")
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "sync", "verify"))
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    args = parser.parse_args()
    try:
        status = run(args.action, Path(__file__).resolve().parents[1], args.codex_home)
    except (OSError, ValueError, tomlkit.exceptions.ParseError) as error:
        parser.exit(1, f"{error}\n")
    parser.exit(status)


if __name__ == "__main__":
    main()
