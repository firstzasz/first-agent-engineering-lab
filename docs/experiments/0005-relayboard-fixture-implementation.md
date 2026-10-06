# EXP-0005: RelayBoard pilot fixture implementation

Status: IMPLEMENTED, CI verification pending

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

Pending PR and CI evidence.

## Limitations

- The fixture is intentionally small and synthetic.
- WSGI/SQLite choices may interact differently with specific agent priors than another stack.
- Evaluator secrecy is workspace/protocol isolation, not cryptographic secrecy.
- No methodology treatment has run yet.

## Result

Pending CI verification.

## Recommendation

If CI is green, freeze the fixture merge commit as the common starting SHA and begin the neutral pilot before any named methodology treatment.
