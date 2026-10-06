# Neutral Control Pilot Runs

Status: READY TO EXECUTE

Treatment: `neutral-v0`

Frozen base SHA (Pilot Start State v0.1):

`2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`

Planned first runs:

- `N-S01-001` -> S01-v0
- `N-S02-001` -> S02-v0.1
- `N-S04-001` -> S04-v0

## Prepared branches

- `N-S01-001`: `treatment/neutral/N-S01-001`
- `N-S02-001`: `treatment/neutral/N-S02-001`
- `N-S04-001`: `treatment/neutral/N-S04-001`

These branch trees were checked after creation and contain no evaluator/oracle/reference-solution paths.

See [Neutral Pilot Execution Handoff](../../../docs/benchmarks/NEUTRAL_EXECUTION_HANDOFF.md).

## Execution rule

Each run must use a fresh agent context that has not seen:

- `experiments/relayboard/evaluator/`
- S02 operator oracle answers;
- S04 root-cause oracle;
- prior treatment outcomes for the same scenario.

Use the treatment runner to prepare the workspace.

Record the exact model and host. Prefer the same model/host across the three neutral runs where practical.

Do not add methodology instructions beyond the task prompt and ordinary host defaults.

## Why this chat cannot be the neutral treatment

The current research session has already inspected the evaluator oracle and injected S04 root cause.

Using this session as the neutral agent would contaminate the experiment.

A separate fresh context is therefore required.

## After each run

1. preserve operator interactions;
2. preserve any agent checkpoints;
3. evaluate with `evaluate_workspace.py`;
4. store the run record and evaluation;
5. do not tune the next scenario based on the result.
