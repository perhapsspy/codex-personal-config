# Codex Personal Config

Private portable Codex instructions for `perhapsspy`.

Clone this repo on a machine, then install only the portable files into that machine's local Codex home:

- `codex/AGENTS.md` -> `~/.codex/AGENTS.md`
- `codex/agents/*.toml` -> `~/.codex/agents/*.toml`

It does not sync the whole `~/.codex` directory. Do not commit auth, sessions, caches, plugin state, memories, local project trust lists, or app-generated machine paths.

## Windows Install

From PowerShell in the repo root:

```powershell
.\scripts\install.ps1
```

If PowerShell blocks local scripts, run this once in that shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

`config.toml` stays machine-local. If you need a small Windows starting point, copy this by hand into `%USERPROFILE%\.codex\config.toml` and adjust locally:

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[windows]
sandbox = "elevated"

[agents]
max_threads = 6
max_depth = 1
```

## Update Flow

1. Edit the shared files in this repo.
2. Commit and push.
3. Pull on the other machine.
4. Run `.\scripts\install.ps1`.

Direct edits in `~/.codex` are fine for experiments. Promote only portable changes back into this repo.
