# RelayBoard Evaluator Material

This directory is evaluator-only during controlled treatment runs.

It is committed publicly for reproducibility, but must not be mounted into the treatment workspace.

A treatment that deliberately reads these files during a run is marked CONTAMINATED.

Frozen pilot evaluator artifacts:

- `S02_OPERATOR_ORACLE_V0.json`
- `S04_ROOT_CAUSE_ORACLE_V0.md`

Later executable evaluator tests must implement these frozen intents without changing them after treatment results are observed.
