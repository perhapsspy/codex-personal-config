# Codex Personal Config

Private, portable Codex configuration for `perhapsspy`.

This repo is meant to be cloned on each machine and installed into that machine's local Codex home. It intentionally does not sync the whole `~/.codex` directory because Codex stores auth, sessions, caches, plugin state, local paths, and machine-specific config there.

## What This Installs

- `codex/AGENTS.md` -> `~/.codex/AGENTS.md`
- `codex/agents/*.toml` -> `~/.codex/agents/*.toml`

It does not install `config.toml` by default. Use `config/*.example` as a starting point and keep machine-specific paths local.

## Windows Setup

Clone this private repository, then run PowerShell from the repo root:

```powershell
.\scripts\install.ps1
.\scripts\validate.ps1
```

If PowerShell blocks local scripts, run this once in that shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

For native Windows Codex, start from `config/windows.toml.example` and copy only the settings you actually want into `%USERPROFILE%\.codex\config.toml`.

## macOS Setup

From the repo root:

```bash
./scripts/install.sh
./scripts/validate.sh
```

## Sync Workflow

1. Edit files in this repo, not directly in `~/.codex`, when the change should be shared across machines.
2. Run validation.
3. Commit and push.
4. Pull on the other machine and run the matching install script.

Direct edits in `~/.codex` are fine for experiments, but promote only the portable parts back into this repo.

## Portable Files

These files should stay portable:

- `codex/AGENTS.md`
- `codex/agents/code-mapper.toml`
- `codex/agents/deep-reasoner.toml`
- `codex/agents/docs-researcher.toml`
- `codex/agents/reviewer.toml`
- `codex/agents/routine_worker.toml`

Avoid committing:

- `auth.json`
- session logs
- memory or cache directories
- plugin cache directories
- app-generated absolute paths
- project trust entries from one machine
