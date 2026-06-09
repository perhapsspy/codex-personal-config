## Repository Purpose

- This repository is the portable source for personal Codex startup guidance and custom support-agent definitions.
- Keep installable files under `codex/`; `scripts/install.ps1` copies them into the local Codex home.
- Do not add Codex runtime state, auth tokens, session logs, caches, plugin caches, memory dumps, or machine-specific project trust lists.

## Editing Rules

- Keep `codex/AGENTS.md` short and behavior-changing only.
- Keep `codex/agents/*.toml` portable across macOS and Windows; avoid absolute local paths unless the agent role explicitly needs them.
- Do not install or sync `config.toml`; document small examples in `README.md` only.
- Update `README.md` and `scripts/install.ps1` when file layout or install behavior changes.

## Validation

- When changing agent files, verify each TOML has `name`, `description`, and `developer_instructions`; on Windows, run `.\scripts\install.ps1` after pulling.
