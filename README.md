# RelayBoard Fixture

Status: EXECUTABLE PILOT FIXTURE IMPLEMENTED, CI verification pending

RelayBoard is the shared synthetic application used by the first FIRST Agent Engineering Lab benchmark scenarios.

It contains no production FIRST logic, credentials, private endpoints, financial records, or personal data.

## Runtime

The base fixture uses Python standard library components only:

- SQLite in-memory persistence;
- a small WSGI API and dashboard;
- deterministic synthetic seed data;
- `unittest` public tests.

The base intentionally contains the pre-treatment state for S01/S02/S04. Evaluator self-tests must prove those scenarios are red-capable while public baseline tests remain green.

## Pilot scope

The first implementation slice supports only:

- S01: tiny reversible change;
- S02: ambiguous product requirement;
- S04: deterministic hard bug.

Other designed scenarios remain out of scope until the pilot harness is validated.

## Intended shape

RelayBoard is a small job-control application with:

- Jobs;
- Runs;
- Attempts;
- retry policy;
- alert rules;
- a minimal operator dashboard;
- deterministic storage and tests.

The implementation should remain small enough that a reviewer can inspect the whole system.

## Pausing Jobs

`POST /api/jobs/{id}/pause` and `POST /api/jobs/{id}/resume` require no
request body. Both return HTTP 200 with the updated `job`, including its
boolean `paused` field; repeating either operation is safe. Unknown Jobs
return HTTP 404 using the existing API error format.

Pause is separate from `enabled`. While paused, new scheduled starts return
HTTP 409 and are skipped without queuing work. Manual Runs remain allowed,
and active Runs continue with their existing retry and alert behavior.
Resume clears pause without changing `enabled` or starting any work, so a
disabled Job remains unschedulable. The dashboard shows pause separately
from enabled state and last result.

Run the public checks with `python -m unittest discover -s tests -v`.

## Treatment isolation

Treatment agents receive the fixture workspace and scenario prompt.

They do **not** receive the evaluator directory as part of the task workspace.

The lab repository is public, so this is protocol isolation rather than cryptographic secrecy. A treatment that deliberately looks up evaluator material is contaminated and must be marked invalid.

See:

- [GLOSSARY.md](./GLOSSARY.md)
- [benchmark scoring](../../docs/benchmarks/SCORING_V0.md)
- [evaluator protocol](../../docs/benchmarks/EVALUATOR_PROTOCOL_V0.md)
