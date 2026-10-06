# EXP-0003: Freeze FIRST-mode v0

Status: IMPLEMENTED, runtime not started

Date: 2026-10-06

## Hypothesis

A FIRST-specific operating contract can be made precise enough to serve as a reproducible experiment treatment without turning it into a production standard.

## Setup

Inputs:

- ADR-0001 contextual fit;
- ADR-0002 portable skill engineering;
- ADR-0003 capability-adaptive legible autonomy;
- Skill Anatomy Matrix v0;
- Mechanism Benchmark Design v0;
- requirement-discovery tradeoff analysis.

No runtime benchmark was executed.

## Implementation

Created:

- `docs/approaches/FIRST_MODE_V0.md`
- `docs/adrs/0004-freeze-first-mode-v0.md`

The treatment specifies:

- decision-authority classification;
- four scaffolding levels;
- structural uncertainty triggers;
- alternative-search rules;
- model-capability adaptation;
- legible checkpoints;
- persistent-state contract;
- verification and debugging contracts;
- orchestration rules;
- completion-status vocabulary;
- freeze/versioning rules.

The benchmark comparison is updated to include four system-level arms:

- neutral control;
- pstack;
- Matt Pocock;
- FIRST-mode v0.

## Expected behavior

A future agent should be able to run FIRST-mode v0 from the frozen document without relying on this chat to reconstruct its philosophy.

## Observed behavior

The current research decisions can be expressed as an inspectable operating contract with explicit triggers and outputs.

## Evidence

- `docs/approaches/FIRST_MODE_V0.md`
- `docs/adrs/0004-freeze-first-mode-v0.md`
- `docs/comparisons/mechanism-benchmark-design-v0.md`
- PR #5
- merge commit: `0cd8eaa5bc0708f6dc1ad507591579016dc91758`

## Limitations

- No treatment has been executed.
- Thresholds for L0-L3 are design hypotheses.
- Capability adaptation has no calibration dataset yet.
- Operator-learning value is not yet measured.
- FIRST-mode contains mechanisms influenced by existing approaches; it is a composition, not a claim of wholly novel invention.

## Result

SUPPORTED for treatment specification only.

## Recommendation

Freeze prompts, oracle intent, and scoring for S01/S02/S04 next, then run the neutral control before any named methodology treatment.
