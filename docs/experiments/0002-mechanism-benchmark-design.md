# EXP-0002: Mechanism benchmark design

Status: IMPLEMENTED, runtime not started

Date: 2026-10-06

## Hypothesis

The lab can translate static skill-anatomy findings into scenario-level experiments that isolate mechanisms and measure operator fit without prematurely building a large benchmark application.

## Setup

Inputs:

- Skill Anatomy Matrix v0
- contextual-fit ADR
- skill-engineering ADR
- pinned pstack and Matt Pocock source snapshots

No runtime treatment was executed.

## Implementation

Created `docs/comparisons/mechanism-benchmark-design-v0.md`.

The design defines a shared synthetic system, RelayBoard, and eight scenarios:

- tiny reversible change;
- ambiguous requirement;
- architecture under uncertainty;
- deterministic hard bug;
- verification trap;
- session interruption/pickup;
- long autonomous run;
- parallel dependency graph.

The first implementation slice is intentionally limited to S01, S02, and S04.

## Expected behavior

The design should make each experiment falsifiable, measurable, and aligned with FIRST's operator preferences while preserving correctness, verification, and safety as hard constraints.

## Observed behavior

The static mechanism hypotheses map cleanly to distinct scenarios. The design can separate repository-level comparisons from mechanism-level treatments.

## Evidence

- `docs/comparisons/mechanism-benchmark-design-v0.md`
- `docs/comparisons/skill-anatomy-matrix-v0.md`

## Limitations

- RelayBoard does not exist yet.
- Metrics have definitions but no calibration data.
- Time/token measurements may vary by host and model.
- Hidden oracle implementation has not started.
- Scenario realism is a design judgment until pilot runs expose missing complexity.

## Result

SUPPORTED for experiment design only.

## Recommendation

Implement the smallest RelayBoard slice needed for S01, S02, and S04, then pilot the neutral baseline before installing or adapting upstream workflows.
