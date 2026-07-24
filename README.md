# Codex Personal Config

Portable personal Codex guidance and custom support-agent definitions for `perhapsspy`.

This repository is the shared source for files that should follow you between machines:

- `codex/AGENTS.md` -> `~/.codex/AGENTS.md`
- `codex/agents/*.toml` -> `~/.codex/agents/*.toml`

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

The installer copies the shared `AGENTS.md` and agent TOMLs. It records the agent filenames it installs in a local `.codex-portable-agent-files` file, then removes only files that a previous run of this installer deployed but the repository has since removed or renamed. It never deletes untracked local agents and never changes `config.toml`.

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

The sync command replaces the repository's `codex/AGENTS.md` and every `codex/agents/*.toml` with the current local counterparts. Keep experiments or machine-only agents out of `~/.codex/agents` before running it, then inspect `git diff`, validate, commit, and push. It does not read or copy `config.toml`.

## Shared configuration flow

1. Adjust the shared guidance or agents on one machine.
2. Run the sync command above.
3. Review `git diff`; verify each TOML has `name`, `description`, and `developer_instructions`.
4. Commit and push this repository.
5. On another machine, pull and run the installer.

## Machine-local configuration

Keep `config.toml` local. If you need a small starting point, copy this by hand and adjust it per machine:

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[agents]
max_threads = 8
max_depth = 1
default_subagent_model = "gpt-5.6-sol"
default_subagent_reasoning_effort = "medium"
```

The defaults apply only when a spawn or custom agent does not select its own model or reasoning effort. Portable decision, review, implementation, and exploration agents keep the explicit settings in their TOML files.

On native Windows, add this when the elevated sandbox is available:

```toml
[windows]
sandbox = "elevated"
```
