# EXP-0004: Freeze RelayBoard pilot scenarios

Status: IMPLEMENTED, runtime not started

Date: 2026-10-06

## Hypothesis

S01, S02, and S04 can be frozen tightly enough to build the fixture without later changing the benchmark to favor a methodology.

## Setup

Inputs:

- Mechanism Benchmark Design v0;
- FIRST-mode v0;
- common operator-interaction taxonomy;
- public-repository safety rules.

No runtime treatment was executed.

## Implementation

Frozen:

- RelayBoard base domain glossary;
- S01-v0 prompt and oracle intent;
- S02-v0 prompt, ambiguity classes, operator protocol, and exact operator answer sheet;
- S04-v0 prompt, root-cause mechanism, false-fix traps, and evaluator intent;
- common scoring rubric;
- evaluator isolation/contamination protocol.

## Expected behavior

Fixture implementation can now proceed against stable scenario requirements.

## Observed behavior

The three pilot scenarios can share one small synthetic domain while stressing different properties:

- S01: process overhead;
- S02: requirement authority and operator burden;
- S04: evidence-first debugging and false-fix resistance.

## Evidence

- `fixtures/relayboard/GLOSSARY.md`
- `docs/benchmarks/SCORING_V0.md`
- `docs/benchmarks/EVALUATOR_PROTOCOL_V0.md`
- `docs/benchmarks/S01_TINY_CHANGE.md`
- `docs/benchmarks/S02_AMBIGUOUS_REQUIREMENT.md`
- `docs/benchmarks/S04_HARD_BUG.md`
- `experiments/relayboard/evaluator/`
- PR #6
- merge commit: `4cc72de0c88a70195d05ed2d9ae05ba73656102c`

## Limitations

- No executable fixture exists yet.
- Public GitHub cannot provide cryptographic oracle secrecy; isolation is procedural and workspace-based.
- Timing and token metrics depend on host instrumentation.
- S02's four product decisions are synthetic and may not represent every real product ambiguity.

## Result

SUPPORTED for scenario freeze only.

## Recommendation

Implement the minimal RelayBoard fixture exactly against these frozen scenario contracts, add executable public/evaluator tests, and verify the harness before running any methodology treatment.
