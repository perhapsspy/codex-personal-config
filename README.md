# Codex Personal Config

Portable personal Codex guidance and custom support-agent definitions for `perhapsspy`.

This repository is the shared source for files that should follow you between machines:

- `codex/AGENTS.md` -> `~/.codex/AGENTS.md`
- `codex/agents/worker.toml` -> `~/.codex/agents/worker.toml`
- `codex/agents/explorer.toml` -> `~/.codex/agents/explorer.toml`

Do not sync the whole `~/.codex` directory. Auth, sessions, caches, memories, plugin state, app-generated paths, and project trust lists stay local. `config.toml` is also machine-local because it commonly contains platform paths and device-specific choices.

## Apply the repository on a machine

Run the installer from the repository root after pulling changes.

macOS or Linux:

```bash
./scripts/install.sh
```

Windows PowerShell:

```powershell
.\scripts\install.ps1
```

If PowerShell blocks local scripts, run this once in that shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

The installer copies the shared `AGENTS.md` and the two managed agent TOMLs. It removes only stale agents previously installed by this repository and leaves other local agents and `config.toml` untouched.

To install into a non-default Codex home, set `CODEX_HOME` on macOS/Linux or pass `-CodexHome` in PowerShell.

```bash
CODEX_HOME="$HOME/.codex-test" ./scripts/install.sh
```

```powershell
.\scripts\install.ps1 -CodexHome "$HOME\.codex-test"
```

## Promote local shared settings into this repository

When you intentionally update the shared settings on a machine, run the sync command from this repository.

macOS or Linux:

```bash
./scripts/sync-from-local.sh
```

Windows PowerShell:

```powershell
.\scripts\sync-from-local.ps1
```

The sync command replaces the repository's `codex/AGENTS.md`, `worker.toml`, and `explorer.toml` with their local counterparts. Other local agents and `config.toml` are ignored. If a required file is missing or invalid, the command stops before updating the repository.

## Shared configuration flow

1. Adjust the shared guidance or managed agents on one machine.
2. Run the sync command above when the source change began in the local Codex home.
3. Run the repository validation:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. Review `git diff`.
5. Commit and push this repository.
6. On another machine, pull and run the installer.

Validation checks the portable agent contracts and install/sync behavior.

## Delegation roles

- `worker` uses Sol Medium for bounded implementation, fixes, refactoring, and tests.
- `explorer` uses Luna Max for code or documentation investigation, log analysis, and checks against explicit criteria.

These are two role definitions, not a two-task limit. Independent work can reuse a role. The main Astra session retains requirements, design, difficult debugging, integration, and final judgment.

## Machine-local configuration

Keep `config.toml` local. Merge this example into the existing file rather than creating a second `[agents]` table:

```toml
model = "gpt-6-astra"
model_reasoning_effort = "xhigh"

[agents]
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-5.6-sol"
default_subagent_reasoning_effort = "medium"
```

The role TOMLs set the model and effort for `worker` and `explorer`; Sol Medium is the fallback for children without an explicit model. Installing or syncing this repository does not change local `config.toml`, other machine-local settings, or personal agents.
