## Runtime Defaults

- Treat `~/.codex/config.toml` as the source of truth for model, reasoning, sandbox, approval, MCP, plugin, and trusted-project defaults.
- Verify current Codex docs before changing global routing, agent, or config behavior; remove stale profiles or plugin entries instead of documenting around them.

## Browser Hygiene

- Browser checks use the Codex in-app browser. Use Playwright only when the user explicitly asks.
- For browser/process cleanup, inspect with shell tools; do not load Playwright MCP/browser tools unless browser automation is explicitly requested.
- After Playwright/Chrome automation, close the browser/context; terminate leftover automation MCP/browser servers (`npm exec @playwright/mcp`, `playwright-mcp`, Playwright `cliDaemon`, `playwright_chromiumdev_profile-*`, automation-launched Chrome helpers). Verify with platform-appropriate process inspection such as `pgrep` on Unix or `Get-Process` on Windows.
- Do not kill the user's normal Chrome session; target only automation profiles or confirmed orphaned helpers.

## Codex Process Safety

- Do not kill Codex app, `codex app-server`, or `Codex Helper` during routine cleanup.
- Codex-owned cleanup requires explicit user request, exact target PIDs, current app/server excluded by default, no broad process-name kills against Codex itself, and post-cleanup verification that Codex stayed running.

## Context Budget

- Keep global instructions short; route repeatable procedures to skills and project/task state to repo docs.
- Start read-heavy work with summaries and bounded reads before full files, diffs, logs, or command output.
- For authorized long multi-agent work, keep the main thread summary-first and route noisy bounded exploration to read-only support agents.

## Support Agents

- Follow the current Codex subagent tool/docs for spawn authorization, orchestration, waiting, and cleanup; do not duplicate those mechanics here.
- When the user authorizes subagents for a task/session, treat that authorization as covering bounded support-agent use until the task ends or the user narrows scope.
- Use `code_mapper` for code paths, `docs_researcher` for primary-source docs/version/policy verification, `deep_reasoner` for bounded hard judgment after initial facts are available, `reviewer` for correctness review, and `routine_worker` only for isolated validated edits.
- Treat user wording such as "딥플레너", "deep planner", or "deep thinking agent" as a request for `deep_reasoner`; the role is deep reasoning, not plan-writing.
