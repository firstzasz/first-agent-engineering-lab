# Run state

Method: FIRST-mode v0, exact frozen canonical text supplied in METHOD.md (no separately named FIRST_MODE_V0.md in supplied area). Route: L1 legible autonomous engineering, L3 only for unresolved product semantics; operator answer received before implementation. No helpers assigned.

Goal / success predicate: POST pause/resume persists a separate Job pause state, repeated operations are safe, unknown Jobs follow 404 conventions; a paused scheduled start returns the existing scheduling-conflict response and creates no Run or queue; manual Runs remain allowed; active Runs continue retries and terminal outcomes with existing alerts unchanged; resume restores scheduling only for enabled Jobs; dashboard and existing enabled/last-result fields retain their meaning. Verify using executable public regression and WSGI API tests, including a red/green cycle.

Grounding: TASK.md, METHOD.md, GLOSSARY.md, README.md, pyproject.toml; relayboard models/store/service/web/testing/main and tests/test_public.py. Existing schedule block uses JobNotSchedulable -> HTTP 409. Existing retries emit failure alerts before terminal failure; preserve this behavior rather than fix the unrelated behavior.

Decisions: PRODUCT_PREFERENCE manual/active Run semantics were escalated to operator, recorded in operator-interactions.json. REVERSIBLE_ENGINEERING: independent persisted paused flag preserves enabled/disabled state; resume does not automatically run anything; default false preserves old Job constructors; paused indicator is a separate dashboard column retaining enabled and last result. Store schema initialization will migrate existing jobs tables to add default-false paused state. FACT: existing synchronous execution has no queued-work subsystem.

Blast radius: Job model, SQLite store, scheduling service, JSON API, dashboard. Integration tests will use the actual WSGI application surface. Independent executable evidence uses deterministic assertions and preserved command outputs; no second agent required for this small reversible fixture. No architectural alternative trigger beyond inspecting those boundaries; conflating pause with enabled would destroy prior disabled state, so a separate flag is selected.

Initial verification: five baseline public tests passed. Remaining: add red tests, implement, run public suite and inspect artifact diff, commit locally.

Boundary: only this supplied area inspected; no evaluator, oracle, reference solution, peer status, lab history or credentials accessed. Manifest model/reasoning fields are requested configuration, not observed identity or usage; actual identity/usage unknown.

Completion: IMPLEMENTED and VERIFIED under the public success predicate. New tests were red (8 failures including subtests, 1 error) before implementation while five baseline tests stayed green; all 13 tests passed after implementation. Artifact diff and whitespace check passed. Implementation commit: 236fc3e6033c261b44a8a970e08a8629ed7e7e5c. No application work remains; evidence is being finalized and committed separately.
