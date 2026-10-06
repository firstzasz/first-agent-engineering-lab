# EXP-0007: Evaluator positive-path validation

Status: IMPLEMENTED, CI verification pending

Date: 2026-10-07

## Hypothesis

The RelayBoard evaluator should be able to prove both directions:

- the frozen base is detectably unsolved;
- a known-good reference implementation is accepted.

Testing only the red path could leave an impossible or contradictory benchmark.

## Setup

No LLM treatment is executed.

Reference patches live under evaluator-only material and are excluded from treatment workspaces.

## Implementation

Added reference solutions for:

- S01-v0;
- S02-v0.1;
- S04-v0.

Added `solution_selftest.py`, which:

1. copies the current fixture into a temporary workspace;
2. applies the evaluator-only reference patch;
3. runs public tests;
4. runs the matching evaluator oracle;
5. requires both to pass.

Also corrected a pre-treatment harness defect: a public baseline test asserted the old S01 heading, which would have made the intended S01 solution fail the public suite. The public test now checks the dashboard contract without freezing the label under change.

## Expected behavior

CI must show:

- base red-capability remains valid;
- public base tests remain green;
- treatment-runner isolation remains green;
- all three reference solutions are accepted by public + evaluator checks.

## Evidence

Pending CI.

## Limitations

Reference implementations prove evaluator satisfiability, not uniqueness or methodology quality.

Because the repository is public, reference patches are protected by treatment workspace isolation and contamination rules rather than secrecy.

## Result

Pending CI verification.

## Recommendation

If green, version the corrected fixture as Pilot Start State v0.1 before executing any neutral treatment.
