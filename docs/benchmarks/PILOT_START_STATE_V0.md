# RelayBoard Pilot Start State v0

Status: FROZEN AND VERIFIED

Date frozen: 2026-10-06

## Common starting commit

`3a3315c3647474a03842d9405bb9a23aa41681b6`

This commit is the common starting state for the first controlled RelayBoard treatment round.

Scenario versions:

- S01-v0
- S02-v0.1
- S04-v0

## Verified harness state

GitHub Actions run:

- workflow: `RelayBoard harness`
- run id: `37469311303`
- event: `push`
- conclusion: `success`

Verified properties:

1. public fixture tests pass from the merged starting commit;
2. evaluator self-test proves all three scenarios are red-capable on the untouched starting fixture.

Observed evaluator red signals:

- S01-v0: `latest_result_heading_missing`, `old_heading_still_present`
- S02-v0.1: `pause_interface_missing`
- S04-v0: `retry_terminal_failure_alert_count=2`, `distinct_runs_not_independently_alerted`, `successful_run_emitted_failure_alert`

## Treatment workspace contract

Each treatment starts from the fixture tree at the frozen commit.

Treatment workspace includes:

- `fixtures/relayboard/`
- the selected scenario prompt;
- the selected methodology instructions;
- normal host tools allowed by that treatment.

Treatment workspace excludes:

- `experiments/relayboard/evaluator/`
- evaluator answer sheets;
- root-cause oracle;
- evaluator test implementation.

The full lab repository remains public for reproducibility. Deliberately fetching evaluator material during a treatment is a protocol violation and marks the run **CONTAMINATED**.

## Baseline public verification command

```bash
PYTHONPATH=fixtures/relayboard \
python -m unittest discover \
  -s fixtures/relayboard/tests \
  -v
```

At the frozen start commit, this command passes.

## Lab-side red-capability command

The following command is for evaluator/harness validation, not treatment agents:

```bash
PYTHONPATH=fixtures/relayboard \
python experiments/relayboard/evaluator/harness_selftest.py
```

At the frozen start commit, this command exits successfully only because it confirms that each scenario's evaluator would currently detect the intended unsolved condition.

## Freeze rule

Do not mutate this starting commit.

Any fixture correction after a controlled treatment begins requires a new start-state version and a new comparison round.

Treatment outputs must be based on this exact SHA or be explicitly marked as a different experiment version.
