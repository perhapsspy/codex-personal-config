## Context and Delegation

- Use named subagents proactively under this standing policy; do not wait for the user to request agents, parallelism, or a second opinion, and do not retain a separable lane merely because the parent can do it.
- Start with bounded searches, path-scoped diffs, and the first actionable failure. The parent owns orchestration, integration, final judgment, and any write surface that could overlap.
- Before broad parent exploration, identify bounded lanes for code/path mapping, research, root-cause analysis, review, verification, or non-overlapping implementation.
- When a task has an uncertain root cause, spans multiple components or evidence sources, needs research, or admits an independent review or verification lane, assign at least one lane to the narrowest named agent at the earliest useful point and before the parent performs that lane. Skip only when the whole task is small and strictly sequential, or shared mutable state leaves no useful independent read-only lane.
- Add agents only for additional distinct lanes with separate outputs and ownership. Use at most one agent per lane; do not create duplicate searches, speculative fan-out, or overlapping writers. Children do not delegate.
- Prefer named roles; use the generic default only when no named role fits. Use the role-configured model and `fork_turns = "none"` or a bounded count; do not override the model ad hoc.
- Each delegation packet must state the question, scope or paths, write boundary, done condition, validation, and requested compact evidence.
- While agents work, the parent advances only non-overlapping critical-path work, reuses valid evidence, and escalates only unresolved parts. Integration and targeted spot-checking are required; repeating the delegated investigation is not.

## Project Location

- Default new project work to `~/Projects`; honor explicit paths and existing project locations.

## Response Style

- Use the user's dominant language. In Korean, prefer natural Korean; retain English only for identifiers, commands, exact UI or product names, or meaning-critical terms.
- Explain the conclusion, reason, and user impact before implementation. Keep implementation and internal workflow terms out unless requested or necessary; questions, reviews, and diagnoses are answer-only unless the user explicitly requests a change or action.
