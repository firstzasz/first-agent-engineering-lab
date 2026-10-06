# EXP-0007: Evaluator positive-path validation

Status: VERIFIED

Date: 2026-10-07

## Hypothesis

The RelayBoard evaluator should be able to prove both directions:

- the frozen base is detectably unsolved;
- a known-good reference implementation is accepted.

Testing only the red path could leave an impossible or contradictory benchmark.

## Setup

No LLM treatment is executed.

Reference solutions live under evaluator-only material and are excluded from treatment workspaces.

## Implementation

Added reference solutions for:

- S01-v0;
- S02-v0.1;
- S04-v0.

Added `solution_selftest.py`, which:

1. copies the current fixture into a temporary workspace;
2. applies the evaluator-only reference solution overlay;
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

- PR #9
- merge commit: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`
- GitHub Actions run: `37547999430`
- `public-tests`: PASS
- `evaluator-red-capability`: PASS
- `treatment-runner`: PASS
- `reference-solutions`: PASS
- reference-solutions log confirmed all three frozen reference implementations were accepted

## Limitations

Reference implementations prove evaluator satisfiability, not uniqueness or methodology quality.

Because the repository is public, reference solution overlayes are protected by treatment workspace isolation and contamination rules rather than secrecy.

## Result

SUPPORTED.

The evaluator is both red-capable on the unsolved base and green-capable on known-good implementations for all three pilot scenarios.

## Recommendation

Use Pilot Start State v0.1 for all first-round treatment workspaces. Do not use the superseded v0 state.
