# Authority-Guided Product Decision Frontier v0

Use this compact procedure for requirement uncertainty. It combines explicit decision authority with an unresolved-product-decision frontier.

## Authority

For each material uncertainty classify it as:

- **FACT**: discover from supplied code/tests/docs; do not ask the operator.
- **REVERSIBLE_ENGINEERING**: decide autonomously; record only if materially useful.
- **PRODUCT_OR_PREFERENCE**: operator-owned externally visible behavior not determined by supplied evidence.
- **IRREVERSIBLE_OR_SECURITY**: gate rather than guess.
- **TRUE_BLOCKER**: report when required information/capability is genuinely unavailable.

## Frontier

1. Inspect the supplied task and workspace.
2. Build a frontier containing only unresolved **PRODUCT_OR_PREFERENCE** decisions.
3. Ask only for decisions on that frontier, grouping related decisions when natural.
4. After every operator answer or material evidence discovery, recompute the frontier.
5. Do not commit behavior that depends on an unresolved frontier item.
6. Continue autonomous work that is independent of unresolved operator-owned decisions.
7. Stop asking when the frontier is empty.

Do not escalate FACT or REVERSIBLE_ENGINEERING items.

This treatment adds no specification/ticket workflow, no mandated subagents, and no review ceremony beyond ordinary host behavior.
