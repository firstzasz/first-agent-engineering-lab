# G2 — Dependency Decision Graph v0

Purpose: improve requirement discovery by decomposing changed behavior into concrete dependent decisions before implementation.

Use only the assigned task, supplied workspace, code, tests and documentation.

Before committing externally visible behavior:

1. State the top-level externally visible behavior being changed.
2. Decompose that behavior into concrete decision branches using the actual domain concepts, state transitions and public/code seams you discover.
3. Continue decomposition until each leaf can be resolved by:
   - supplied evidence/fact investigation,
   - ordinary reversible engineering judgment, or
   - an operator-owned product/preference decision.
4. Record prerequisite edges when the answer to one leaf changes which downstream leaves exist or can be asked meaningfully.
5. Resolve fact and reversible-engineering leaves yourself.
6. Ask the operator only currently unblocked product/preference leaves.
7. After each material answer or evidence discovery, recompute dependent branches.
8. Stop only when every material branch is closed or explicitly blocked.

Do not require an actor/state/timing matrix. Do not import ticketing/specification/review workflows. The dependency graph is a discovery structure, not a requirement source.
