## Repository Purpose

- This repository is the portable source for personal Codex startup guidance.
- Keep installable files under `codex/`; copy them into the local Codex home on each machine.
- Do not add Codex runtime state, auth tokens, session logs, caches, plugin caches, memory dumps, or machine-specific project trust lists.

## Editing Rules

- Keep `codex/AGENTS.md` short and behavior-changing only.
- Manage only the core keys declared in `codex/config.shared.toml`; preserve all other local `config.toml` settings.
- Update `README.md` and install commands when file layout or install behavior changes.

## Validation

- Run `python3 -m unittest discover -s tests -v` after changing shared guidance or install scripts.
- When installable files change, run the installer from `README.md` and verify the installed files and declared settings. Distinguish saved configuration from a running session's effective settings.

## Deployment Targets

- For deployment or sync work, follow the target workflow in `README.md` for the Mac, the dot instance's Codex, and manual Windows installs. Check each accessible target on its actual host; report verified, pending, or blocked status separately. A local install does not verify the dot instance.
- Import shared settings only from the explicitly selected source host. After reviewing and publishing them, install and verify that revision on the other targets; preserve their host-local settings and state.

## Completion

- For completed user-requested changes in this repository, after validation and a scoped diff review, commit the intended files and push the current branch to its configured upstream without asking again unless the user requests local or uncommitted changes. Requests limited to investigation, review, or planning use local links unless publication is requested or required by repository rules.
- Stage only intended paths. Do not include unrelated existing changes, switch branches, rewrite history, or force-push. If safe isolation is impossible or an upstream push fails, stop that operation and report the blocker; continue independent work within scope.
