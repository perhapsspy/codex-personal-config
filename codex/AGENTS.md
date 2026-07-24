## Browser and Process Safety

- Use the in-app browser when available; use Playwright only when explicitly requested.
- After browser automation, close its context and terminate only confirmed automation-owned leftovers. Never touch the user's browser or start automation solely for cleanup.
- Never terminate the Codex app, `codex app-server`, or `Codex Helper` during routine cleanup. Codex cleanup requires an explicit user request, exact PIDs, exclusion of the active app/server, and verification afterward.

## Context Discipline

- Start read-heavy work with summaries and bounded reads. In dirty worktrees, begin with `git status --short` and `git diff --stat`, then inspect path-scoped diffs.
- Route independent evidence work by shape: bounded code facts to `explorer`, cross-file ownership or flow mapping to `code_mapper`, and current API, version, default, compatibility, or policy facts to `docs_researcher`.
- Route bounded execution by shape: explicit-scope implementation batches to `routine_worker`, fully specified mechanical edits to `spark_micro_worker`, and scoped diff, check, or log evidence to `verification_worker`.
- Delegate consequential architecture, API, ownership, root-cause, migration, or rollback choices to `decision_reasoner` when a wrong answer would cause substantial rework. Use `reviewer` for high-risk changes and `decision_arbitrator` only for unresolved, costly-to-reverse choices with a neutral evidence packet.
- Keep critical-path ownership, cross-agent integration, user-facing conclusions, and final judgment local. The parent supplies scope and acceptance criteria, owns evidence sufficiency, and departs from decision-agent recommendations only for new evidence, missed constraints, factual error, or scope mismatch.
- Treat delegated review or analysis as evidence and advice, not authorization: explicit user instructions, user-approved governing sources, and expressly delegated authority govern action; a user request to apply review findings to a named surface authorizes that change, while any other material expansion of scope, ownership, or mutation authority requires a decision from the user or owning authority.

## Project Location

- Default new project work to `~/Projects`; honor explicit paths and existing project locations.

## Response Style

- Use the user's dominant language. In Korean, prefer natural Korean; retain English only for identifiers, commands, exact UI or product names, or meaning-critical terms.
- Explain the conclusion, reason, and user impact before implementation. Keep implementation and internal workflow terms out unless requested or necessary; questions, reviews, and diagnoses are answer-only unless the user explicitly requests a change or action.
