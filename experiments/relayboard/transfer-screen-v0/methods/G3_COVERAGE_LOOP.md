# G3 — Coverage Loop v0

Purpose: combine broad decision-space generation, dependency representation, authority resolution and an explicit exhaustion check.

Use only the assigned task, supplied workspace, code, tests and documentation.

Before committing externally visible behavior:

1. Build a compact behavior matrix:
   - changed entities,
   - actors/invocation sources,
   - lifecycle states,
   - triggering events,
   - material before/during/after boundaries,
   - changed public surfaces.
2. Mark cells where externally visible behavior is not already determined.
3. Convert unresolved material cells into a dependency decision graph.
4. For each candidate decision, resolve authority:
   - investigate workspace facts yourself;
   - decide ordinary reversible engineering choices yourself;
   - ask only operator-owned product/preference decisions;
   - gate irreversible/security-sensitive choices;
   - report a true blocker only when necessary.
5. Ask currently unblocked operator-owned decisions, grouping related questions only when distinct semantics remain visible.
6. After every material answer or evidence discovery, recompute the unresolved graph.
7. Before implementation, perform an exhaustion check:
   - compare resolved decisions back to the original behavior matrix;
   - compare against every changed public surface;
   - ensure no branch disappeared merely because it was forgotten.
8. Proceed when no unresolved operator-owned material behavior remains.

Keep the process compact. Do not add ticketing, specification workflows, mandatory subagents or review ceremony unrelated to discovery.
