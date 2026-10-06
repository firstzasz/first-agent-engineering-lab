# RelayBoard Fixture

Status: DOMAIN FROZEN FOR PILOT, executable fixture not yet implemented

RelayBoard is the shared synthetic application used by the first FIRST Agent Engineering Lab benchmark scenarios.

It contains no production FIRST logic, credentials, private endpoints, financial records, or personal data.

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

## Treatment isolation

Treatment agents receive the fixture workspace and scenario prompt.

They do **not** receive the evaluator directory as part of the task workspace.

The lab repository is public, so this is protocol isolation rather than cryptographic secrecy. A treatment that deliberately looks up evaluator material is contaminated and must be marked invalid.

See:

- [GLOSSARY.md](./GLOSSARY.md)
- [benchmark scoring](../../docs/benchmarks/SCORING_V0.md)
- [evaluator protocol](../../docs/benchmarks/EVALUATOR_PROTOCOL_V0.md)
