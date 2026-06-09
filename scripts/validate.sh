#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  "codex/AGENTS.md"
  "codex/agents/code-mapper.toml"
  "codex/agents/deep-reasoner.toml"
  "codex/agents/docs-researcher.toml"
  "codex/agents/reviewer.toml"
  "codex/agents/routine_worker.toml"
  "scripts/install.ps1"
  "scripts/install.sh"
)

for path in "${required[@]}"; do
  test -f "$repo_root/$path" || {
    echo "Missing required file: $path" >&2
    exit 1
  }
done

python3 - <<'PY' "$repo_root"
import pathlib
import sys
import tomllib

root = pathlib.Path(sys.argv[1])
for path in sorted((root / "codex" / "agents").glob("*.toml")):
    data = tomllib.loads(path.read_text())
    for field in ("name", "description", "developer_instructions"):
        if not data.get(field):
            raise SystemExit(f"{path.name} is missing required field: {field}")
print("Agent TOML validation passed.")
PY

for forbidden in auth.json sessions plugins/cache .tmp; do
  if test -e "$repo_root/$forbidden"; then
    echo "Forbidden runtime state in repo: $forbidden" >&2
    exit 1
  fi
done

echo "Validation passed."
