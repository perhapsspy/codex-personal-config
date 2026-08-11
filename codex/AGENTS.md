## Context and Delegation

- Start with bounded searches, path-scoped diffs, and the first actionable failure.
- The parent owns orchestration, integration, and final judgment.
- Keep work with the parent by default. Delegate only when a clearly separable bounded subproblem is likely to materially improve correctness or reduce critical-path work beyond its coordination cost; use the narrowest named agent and start with one.
- Spawn named agents with `fork_turns = "none"` or a bounded turn count, and select their model through the named role rather than a model override.
- Allow one writer per overlapping surface. Children do not delegate.
- Give scope, write boundary, done condition, and validation; request compact evidence.
- Reuse valid evidence and escalate only the unresolved part. Never spawn to fill capacity.

## Project Location

- Default new project work to `~/Projects`; honor explicit paths and existing project locations.

## Response Style

- Use the user's dominant language. In Korean, prefer natural Korean; retain English only for identifiers, commands, exact UI or product names, or meaning-critical terms.
- Explain the conclusion, reason, and user impact before implementation. Keep implementation and internal workflow terms out unless requested or necessary; questions, reviews, and diagnoses are answer-only unless the user explicitly requests a change or action.
