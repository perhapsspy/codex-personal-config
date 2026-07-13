## Browser and Process Safety

- Use the in-app browser when available; use Playwright only when explicitly requested.
- After browser automation, close its context and terminate only confirmed automation-owned leftovers. Never touch the user's browser or start automation solely for cleanup.
- Never terminate the Codex app, `codex app-server`, or `Codex Helper` during routine cleanup. Codex cleanup requires an explicit user request, exact PIDs, exclusion of the active app/server, and verification afterward.

## Context Discipline

- For read-heavy work, start with summaries and bounded reads; read further when judgment, execution, or verification needs more evidence.
- In dirty worktrees, start with `git status --short` and `git diff --stat`; inspect path-scoped diffs first.
- When a bounded non-trivial decision has enough initial evidence and the choice drives architecture, root cause, ownership, migration or rollback, or material rework, delegate the decision to `decision_reasoner` before committing to a plan. Start it without inherited conversation context and pass a neutral packet with the decision question, user constraints and corrections, verified facts or narrow evidence paths, unknowns, and success or rollback conditions; omit the main thread's preferred conclusion. Skip simple edits, docs lookup, fact gathering, implementation delegation, and final review.
- Use `decision_arbitrator` directly only when a sufficiently evidenced decision is costly to reverse and still has multiple plausible alternatives, or escalate to it when `decision_reasoner` leaves a material conflict despite sufficient evidence. Never use Max reasoning to compensate for missing evidence.
- Keep small immediate critical-path work local. Delegate bounded sidecar or repeatable work only when isolation, scale, or real parallelism offsets startup cost; prefer one `routine_worker` for related known-file changes unless latency justifies disjoint parallel workers.
- Treat subagent output as support by default. For `decision_reasoner` and `decision_arbitrator`, treat the recommendation as the primary reasoning result for the assigned bounded question; depart only for new evidence, a missed user constraint, a factual error, or scope mismatch, and state why. The parent owns evidence sufficiency, user corrections, integration, execution, verification, and final browser/UI/runtime/deployment/local-state claims.

## Project Location

- Default new project work to `~/Projects`; honor explicit paths and existing project locations.

## Language

- When the user specifies a response or document language, write in that language consistently; preserve other-language terms only for proper nouns, code identifiers, official API/product names, and terms with a clear reason to remain untranslated.
