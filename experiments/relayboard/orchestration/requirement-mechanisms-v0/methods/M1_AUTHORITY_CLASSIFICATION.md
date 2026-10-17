# Requirement Authority Classification v0

Use this procedure only to decide who should resolve an uncertainty encountered while implementing the assigned task.

For each material uncertainty, classify it as exactly one of:

- **FACT**: answerable from the supplied code, tests, documentation, or direct inspection. Investigate it yourself. Do not ask the operator.
- **REVERSIBLE_ENGINEERING**: an implementation choice that can be changed later without choosing product behavior for the operator. Decide it yourself. Record it only when materially useful.
- **PRODUCT_OR_PREFERENCE**: externally visible behavior or preference that the supplied evidence does not determine and that belongs to the product/operator. Ask the operator before committing dependent behavior.
- **IRREVERSIBLE_OR_SECURITY**: a materially irreversible or security-sensitive choice. Gate it rather than guessing.
- **TRUE_BLOCKER**: required information or capability is genuinely unavailable. Report the blocker.

Rules:

- Do not ask the operator for FACT or REVERSIBLE_ENGINEERING items.
- Do not silently invent unresolved PRODUCT_OR_PREFERENCE behavior.
- Continue autonomously on work that is not blocked by an unanswered operator-owned decision.
- This treatment adds no decision-frontier loop, no specification workflow, no ticketing process, no mandated subagents, and no review ceremony beyond ordinary host behavior.
