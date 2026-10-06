# EXP-0005: RelayBoard pilot fixture implementation

Status: VERIFIED

Date: 2026-10-06

## Hypothesis

A small Python-standard-library fixture can support S01, S02, and S04 while remaining inspectable and deterministic enough for methodology experiments.

## Setup

The fixture is built only from synthetic data.

No external service, credential, production endpoint, or private FIRST data is used.

The pilot domain and scenario semantics were frozen before implementation.

## Implementation

RelayBoard uses:

- Python standard library only;
- SQLite in-memory persistence;
- a small WSGI API/dashboard;
- deterministic Job/Run/Attempt/Alert behavior;
- public `unittest` coverage;
- evaluator-only scenario probes;
- GitHub Actions harness checks.

The base fixture intentionally starts in the pre-treatment state:

- S01 is red because the dashboard still says `Last result`;
- S02 is red because pause/resume does not exist;
- S04 is red because the retry lifecycle can emit duplicate failure alerts.

Public base tests remain green.

## S02 protocol correction before any run

Fixture design exposed that the original S02-v0 prompt did not define a stable external seam for evaluator interaction.

Before any treatment run, S02 is therefore versioned to **S02-v0.1** and freezes these endpoints:

- `POST /api/jobs/{id}/pause`
- `POST /api/jobs/{id}/resume`

This is an experiment-design correction, not a response to treatment results.

The four product semantics remain unchanged.

## Expected behavior

CI should demonstrate two properties simultaneously:

1. public base tests pass;
2. evaluator self-test proves S01/S02/S04 are red-capable on the frozen base.

## Evidence

- PR #7
- merge commit: `3a3315c3647474a03842d9405bb9a23aa41681b6`
- GitHub Actions run: `37469311303`
- public test job: PASS, 5 tests
- evaluator red-capability job: PASS
- frozen start-state record: `docs/benchmarks/PILOT_START_STATE_V0.md`

## Limitations

- The fixture is intentionally small and synthetic.
- WSGI/SQLite choices may interact differently with specific agent priors than another stack.
- Evaluator secrecy is workspace/protocol isolation, not cryptographic secrecy.
- No methodology treatment has run yet.

## Result

SUPPORTED.

The merged fixture is executable, the public baseline is green, and the evaluator independently demonstrates that S01-v0, S02-v0.1, and S04-v0 begin in detectable unsolved states.

## Recommendation

Use the frozen merge commit as the only pilot starting state. Build the treatment runner and execute neutral controls in fresh evaluator-blind contexts before any named methodology treatment.


## Start-state supersession

The fixture implementation itself was verified at `3a3315c3647474a03842d9405bb9a23aa41681b6`.

Before any LLM treatment, EXP-0007 discovered that one public S01 test contradicted the intended target behavior. The corrected benchmark start state is now Pilot Start State v0.1 at `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.

The original implementation evidence remains valid historical evidence; v0.1 is the required treatment base.
