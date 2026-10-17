# Product Decision Frontier v0

Use this procedure only to ensure unresolved operator-owned product behavior is not silently assumed.

Before implementation commits externally visible behavior:

1. Inspect the supplied task, code, tests, and documentation.
2. Write down the currently unresolved externally visible behavior decisions that cannot be settled from supplied evidence or ordinary reversible implementation judgment.
3. Treat that set as the **product decision frontier**.
4. Ask the operator only for decisions on that frontier. Related decisions may be grouped naturally in one exchange.
5. After each operator answer or relevant evidence discovery, recompute the frontier from the updated understanding.
6. Continue until no unresolved operator-owned product decision remains before committing behavior that depends on it.
7. Work that is independent of the unresolved frontier may continue autonomously.

Do not ask the operator to explain facts discoverable from the workspace or ordinary reversible implementation details.

This treatment adds no full authority taxonomy, no specification/ticket workflow, no mandated subagents, and no review ceremony beyond ordinary host behavior.
