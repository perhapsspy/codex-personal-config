# Codex Personal Config

Private portable Codex instructions for `perhapsspy`.

This repo is the shared source for personal Codex guidance across machines. On any machine, pull the repo and copy only the portable files into that machine's local Codex home:

- `codex/AGENTS.md` -> `~/.codex/AGENTS.md`
- `codex/agents/*.toml` -> `~/.codex/agents/*.toml`

Do not sync the whole `~/.codex` directory. Keep auth, sessions, caches, plugin state, memories, local project trust lists, and app-generated machine paths local.

## Install

PowerShell:

```powershell
.\scripts\install.ps1
```

If PowerShell blocks local scripts, run this once in that shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Unix shell:

```bash
mkdir -p "$HOME/.codex/agents"
cp codex/AGENTS.md "$HOME/.codex/AGENTS.md"
cp codex/agents/*.toml "$HOME/.codex/agents/"
```

`config.toml` stays machine-local. If you need a small starting point, copy this by hand into the local Codex config and adjust per machine:

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[agents]
max_threads = 6
max_depth = 1
```

On native Windows, add this when the elevated sandbox is available:

```toml
[windows]
sandbox = "elevated"
```

## Sync Flow

1. Pull this repo on the machine you are using.
2. Install the portable files into local Codex home.
3. Edit shared guidance in this repo when a change should follow you to other machines.
4. Commit and push.
5. Pull and install on the other machine.

Direct edits in `~/.codex` are fine for experiments. Promote only portable changes back into this repo.
