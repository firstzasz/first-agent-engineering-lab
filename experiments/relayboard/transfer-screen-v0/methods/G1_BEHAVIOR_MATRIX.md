# G1 — Behavior Matrix Generation v0

Purpose: improve requirement discovery by systematically generating candidate behavior cases before implementation.

Use only the assigned task, supplied workspace, code, tests and documentation.

Before committing externally visible behavior:

1. Identify the changed domain entities.
2. Identify relevant actors or invocation sources.
3. Identify lifecycle states and triggering events.
4. Enumerate materially distinct timing boundaries such as before, during and after the change/event.
5. Identify changed public/API/dashboard surfaces.
6. Build a compact behavior matrix from the combinations that could plausibly differ in externally visible behavior.
7. For each material cell, determine whether supplied evidence already fixes the behavior, whether it is an ordinary reversible engineering choice, or whether it is genuinely operator-owned product behavior.
8. Investigate evidence-resolvable items yourself.
9. Decide reversible engineering items yourself.
10. Ask the operator only unresolved product/preference cells.
11. After receiving answers, rescan the matrix once for uncovered material cases before implementation.

Do not invent extra ceremony, ticketing, specification documents, subagents or review steps unless ordinary host behavior independently calls for them.

The matrix may be kept as concise working notes. It is a coverage aid, not a requirement source. Do not treat every theoretical combination as a product decision.
