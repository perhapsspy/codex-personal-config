## Browser and Process Safety

- Use the in-app browser when available; use Playwright only when explicitly requested.
- After browser automation, close its context and terminate only confirmed automation-owned leftovers. Never touch the user's browser or start automation solely for cleanup.
- Never terminate the Codex app, `codex app-server`, or `Codex Helper` during routine cleanup. Codex cleanup requires an explicit user request, exact PIDs, exclusion of the active app/server, and verification afterward.

## Context Discipline

- For read-heavy work, start with summaries and bounded reads; read further when judgment, execution, or verification needs more evidence.
- In dirty worktrees, start with `git status --short` and `git diff --stat`; inspect path-scoped diffs first.
- Delegate sufficiently evidenced, bounded decisions that materially affect architecture, root cause, ownership, migration or rollback, or rework to `decision_reasoner`; keep simple edits, lookup, fact gathering, implementation, and final review local.
- Use `decision_arbitrator` only when a costly-to-reverse decision still has multiple plausible alternatives, or when `decision_reasoner` leaves a material conflict. Give decision agents a neutral fresh-context packet; gather missing evidence instead of increasing reasoning effort.
- Keep immediate critical-path work local. Delegate bounded implementation only when isolation, volume, or real parallelism justifies startup cost; use one `routine_worker` for related known-file changes unless the work is genuinely disjoint.
- The parent owns evidence sufficiency, corrections, integration, execution, verification, and final claims. Treat decision-agent recommendations as primary within their assigned boundary; depart only for new evidence, missed constraints, factual error, or scope mismatch.

## Project Location

- Default new project work to `~/Projects`; honor explicit paths and existing project locations.

## Language

- When the user specifies a response or document language, write in that language consistently; preserve other-language terms only for proper nouns, code identifiers, official API/product names, and terms with a clear reason to remain untranslated.
