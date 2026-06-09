## Repository Purpose

- This repository is the portable source for personal Codex startup guidance and custom support-agent definitions.
- Keep installable files under `codex/`; root files explain and validate this repository.
- Do not add Codex runtime state, auth tokens, session logs, caches, plugin caches, memory dumps, or machine-specific project trust lists.

## Editing Rules

- Keep `codex/AGENTS.md` short and behavior-changing only.
- Keep `codex/agents/*.toml` portable across macOS and Windows; avoid absolute local paths unless the agent role explicitly needs them.
- Put OS-specific `config.toml` guidance in `config/*.example`, not in the default install path.
- Update `README.md` and install scripts when file layout or install behavior changes.

## Validation

- On macOS/Linux, run `./scripts/validate.sh`.
- On Windows PowerShell, run `.\scripts\validate.ps1`.
