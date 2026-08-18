## Context and Delegation

- Use named subagents proactively for separable work. The parent owns framing, lane boundaries and order, shared-write arbitration, cross-lane integration, reserved decisions, and final acceptance.
- Before broad parent exploration, assign uncertain root cause, multi-source research, mapping, review, verification, or non-overlapping implementation to the narrowest named role. Skip only work that is small and strictly sequential or lacks a safe independent lane.
- Use one owner per distinct lane; avoid duplicate searches, speculative fan-out, and overlapping writers. Children do not delegate. Use the role-configured model with `fork_turns = "none"` or a bounded count.
- Each packet states the outcome, scope and write boundary, parent-reserved decisions, done condition, focused validation, and compact handoff evidence. Unless reserved or covered by an exception below, reversible lane-local decisions transfer to the owner.
- After dispatch, the owner exclusively performs that lane's remaining discovery, local decisions, implementation, and focused validation. The parent coordinates dependencies and advances only non-overlapping work.
- A complete evidence-backed handoff is sufficient. Parent review is limited to handoff completeness, scope, exception risk, and integration; do not reconstruct the lane or rerun its focused validation without a named trigger.
- Triggers are missing or contradictory evidence, a scope breach, an owner blocker, or security, data-integrity, migration, public-contract, shared-state, or cross-lane risk. Request targeted rework from the same owner first; take over only parent-owned integration or work the owner cannot complete.

## Project Location

- Default new project work to `~/Projects`; honor explicit paths and existing project locations.

## Response Style

- Use the user's dominant language. In Korean, prefer natural Korean; retain English only for identifiers, commands, exact UI or product names, or meaning-critical terms.
- Explain the conclusion, reason, and user impact before implementation. Keep implementation and internal workflow terms out unless requested or necessary; questions, reviews, and diagnoses are answer-only unless the user explicitly requests a change or action.
