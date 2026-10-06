# EXP-0008: Prepare evaluator-blind neutral workspaces

Status: VERIFIED FOR WORKSPACE PREPARATION, treatment execution pending

Date: 2026-10-07

## Hypothesis

Neutral pilot workspaces can be persisted as Git branches whose current trees expose only the fixture, frozen task, public tests, and run metadata, allowing a fresh agent to execute without the evaluator being present in its normal workspace.

## Setup

Frozen treatment base:

`2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`

Runs:

- N-S01-001 / S01-v0
- N-S02-001 / S02-v0.1
- N-S04-001 / S04-v0

No LLM treatment was executed during this experiment.

## Implementation

Created three dedicated treatment branches:

- `treatment/neutral/N-S01-001`
- `treatment/neutral/N-S02-001`
- `treatment/neutral/N-S04-001`

Each branch current tree contains:

- `TASK.md`;
- `GLOSSARY.md`;
- fixture source;
- public tests;
- `pyproject.toml`;
- `.experiment/RUN_MANIFEST.json`;
- `.gitignore`.

The branch trees intentionally omit evaluator material.

## Expected behavior

A fresh coding agent working from one branch should be able to solve the visible task without evaluator files appearing in the branch tree.

## Observed behavior

Recursive Git tree inspection showed no evaluator/oracle/reference-solution path in any of the three prepared commits.

Prepared commits:

- N-S01-001: `563952fab378eda87da696cda4df12fe5c9d4e5e`
- N-S02-001: `2fcdf1702b93bb2beb79add5dc57d8b82e3bda22`
- N-S04-001: `58e55eebad654c357934b93b639e6ba91f6d235d`

## Evidence

- PR #11 merged as `c991b46ffa7aeb5f94c0cbeebcd478c79c2d4d7d`;
- neutral execution issues #12, #13, and #14;
- prepared treatment branches above;
- [Neutral Pilot Execution Handoff](../benchmarks/NEUTRAL_EXECUTION_HANDOFF.md);
- Pilot Start State v0.1;
- runner-repin CI run `37548342313`.

## Limitations

The repository is public and branch history has a parent in the lab repository. An agent with unrestricted repository/web access could deliberately retrieve evaluator material from another ref.

The protocol therefore provides evaluator-blind **workspace isolation**, not cryptographic secrecy.

The current research chat is itself contaminated and cannot act as the neutral treatment agent.

## Result

SUPPORTED for workspace preparation only.

## Recommendation

Execute each neutral run in a fresh context, preserve all run evidence, and evaluate outside the treatment context before starting named methodology arms.
