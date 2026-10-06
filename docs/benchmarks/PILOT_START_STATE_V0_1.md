# RelayBoard Pilot Start State v0.1

Status: FROZEN AND VERIFIED

Date frozen: 2026-10-07

## Common starting commit

`2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`

This commit supersedes Pilot Start State v0 **before any LLM treatment was executed**.

Scenario versions:

- S01-v0
- S02-v0.1
- S04-v0

## Why v0 was superseded

Evaluator positive-path validation found that a public S01 baseline test asserted the old heading `Last result`. That made the intended S01 solution incompatible with the public suite.

Because no treatment had run, the harness was corrected and versioned rather than carrying a known contradictory oracle into the experiment.

The task prompt, S01 evaluator intent, S02 product oracle, and S04 root-cause oracle were not changed in response to treatment outcomes.

## Verified harness state

GitHub Actions run:

- workflow: `RelayBoard harness`
- run id: `37547999430`
- event: `push`
- commit: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`
- conclusion: `success`

Verified properties:

1. public fixture tests pass on the corrected merged start state;
2. evaluator red-capability confirms S01-v0, S02-v0.1, and S04-v0 are detectably unsolved;
3. treatment-runner isolation remains valid;
4. evaluator reference solutions for all three scenarios pass both public tests and the matching oracle.

## Treatment workspace contract

Each treatment starts from the fixture tree at this exact commit.

Treatment workspace includes:

- `fixtures/relayboard/`;
- the selected frozen scenario prompt;
- the selected methodology instructions;
- normal host tools allowed by that treatment.

Treatment workspace excludes:

- `experiments/relayboard/evaluator/`;
- evaluator answer sheets;
- root-cause oracle;
- reference solutions;
- evaluator test implementation.

The full lab repository remains public for reproducibility. Deliberately fetching evaluator material during a treatment marks the run **CONTAMINATED**.

## Freeze rule

Do not mutate this starting state after a controlled treatment begins.

Any later fixture correction requires a new start-state version and a new comparison round.

All pilot run records must use `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f` as `base_sha`.
