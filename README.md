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

## Job pause controls

`POST /api/jobs/{id}/pause` pauses scheduled starts; `POST /api/jobs/{id}/resume`
removes that pause. Both return `200` with a `job` object, or `404` for an
unknown Job, and are idempotent. Job API responses include a `paused` boolean,
and the dashboard shows it alongside Enabled and Last result.

Pause is separate from enabled/disabled state. Resume does not enable a disabled
Job, and enabling a paused Job does not resume it. Scheduled starts require the
Job to be enabled and unpaused, otherwise the Run API returns `409`.
Manual Runs remain allowed while paused. Existing Runs continue to completion,
including their existing retry and alert behavior. Pause/resume creates no Runs,
Attempts, or Alerts. Existing stored Jobs default to unpaused on schema upgrade.

## Treatment isolation

Treatment agents receive the fixture workspace and scenario prompt.

They do **not** receive the evaluator directory as part of the task workspace.

The lab repository is public, so this is protocol isolation rather than cryptographic secrecy. A treatment that deliberately looks up evaluator material is contaminated and must be marked invalid.

See:

- [GLOSSARY.md](./GLOSSARY.md)
- [benchmark scoring](../../docs/benchmarks/SCORING_V0.md)
- [evaluator protocol](../../docs/benchmarks/EVALUATOR_PROTOCOL_V0.md)
