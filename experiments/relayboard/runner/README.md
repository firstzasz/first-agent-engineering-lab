# RelayBoard Treatment Runner

Status: EXPERIMENTAL HARNESS

This runner prepares evaluator-blind workspaces from the frozen RelayBoard start commit and evaluates completed workspaces with the lab-side oracle.

## Frozen start

Pilot start-state version: `v0.1`

`2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`

Supported pilot scenarios:

- `S01-v0`
- `S02-v0.1`
- `S04-v0`

Treatment identifiers:

- `neutral-v0`
- `first-mode-v0`
- `pstack-pinned`
- `matt-pinned`

## Prepare a workspace

```bash
python experiments/relayboard/runner/prepare_workspace.py \
  --scenario S01-v0 \
  --treatment neutral-v0 \
  --host <host-name> \
  --model <model-name> \
  --output /tmp/relayboard-s01-neutral
```

The output is a standalone git repository containing only the fixture, task prompt, and treatment metadata. Evaluator files are not copied.

For FIRST-mode v0, the frozen FIRST-mode document is copied as `METHOD.md`.

For pstack and Matt treatments, the runner records the pinned upstream snapshot but does not copy upstream source. Native installation/adaptation must be handled by the host-specific experiment protocol.

## Execute

Run the treatment in a **fresh context** that has not seen evaluator material.

The agent may inspect everything in its prepared workspace.

It must not deliberately fetch the public lab evaluator files. Doing so marks the run contaminated.

## Evaluate

After the treatment ends:

```bash
python experiments/relayboard/runner/evaluate_workspace.py \
  --scenario S01-v0 \
  --workspace /tmp/relayboard-s01-neutral \
  --output /tmp/s01-neutral-evaluation.json
```

Evaluation runs public tests and the scenario-specific lab oracle against the modified workspace.

## Comparison discipline

For causal comparisons, keep model and host matched when possible.

Native pstack/Matt runs may necessarily include host behavior. Treat those as **system-level results**, not pure methodology effects.

Mechanism-isolation runs are still required to explain causality.
