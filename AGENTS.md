## Repository Purpose

- This repository is the portable source for personal Codex startup guidance and custom support-agent definitions.
- Keep installable files under `codex/`; copy them into the local Codex home on each machine.
- Do not add Codex runtime state, auth tokens, session logs, caches, plugin caches, memory dumps, or machine-specific project trust lists.

## Editing Rules

- Keep `codex/AGENTS.md` short and behavior-changing only.
- Keep `codex/agents/*.toml` portable across macOS and Windows; avoid absolute local paths unless the agent role explicitly needs them.
- Do not install or sync `config.toml`; document small examples in `README.md` only.
- Update `README.md` and install commands when file layout or install behavior changes.

## Validation

- Run `python3 -m unittest discover -s tests -v` after changing shared guidance or agent files.
- When installable files change, run the installer from `README.md` and confirm the repository source matches the installed runtime.

## Completion

- For completed user-requested changes in this repository, after validation and a scoped diff review, commit the intended files and push the current branch to its configured upstream without asking again unless the user requests local or uncommitted changes.
- Stage only intended paths. Do not include unrelated existing changes, switch branches, rewrite history, or force-push. If the change cannot be isolated safely or the upstream push fails, stop and report the exact blocker.
