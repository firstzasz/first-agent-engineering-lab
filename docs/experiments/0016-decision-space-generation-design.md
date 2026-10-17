# EXP-0016: Decision-space generation and transfer-scenario design

Date: 2026-10-18
Status: **IMPLEMENTED AND VERIFIED through transfer-harness validation; no contestant run started**

## Starting evidence

EXP-0014 staged screening produced four valid one-run observations:

- M0 neutral: 2/4 surfaced, 2/4 silent;
- M1 authority classification: 2/4 surfaced, 2/4 silent;
- M2 simplified decision frontier: 2/4 surfaced, 2/4 silent;
- M3 authority + simplified frontier: 2/4 surfaced, 2/4 silent.

All four passed public and frozen evaluator acceptance.

Both earlier Matt-port S02 runs surfaced 4/4 with 0 silent assumptions.

Trace review shows Matt's frozen route used code/domain inspection, concrete scenario reasoning and a dependency/design tree before or alongside frontier traversal.

## Research question

Does explicit **decision-space generation** improve discovery completeness on ambiguous requirements, and does combining generation with dependency representation/exhaustion generalize beyond the original pause/resume task?

## Candidate mechanisms

See [Requirement Discovery Mechanism Model v1](../comparisons/requirement-discovery-mechanism-model-v1.md).

The next candidate arms are:

- G0 Neutral;
- G1 Behavior Matrix Generation;
- G2 Dependency Tree Generation;
- G3 Coverage Loop.

These are research mechanisms only.

## Why new scenarios are required

Repeatedly tuning against S02 risks benchmark-specific overfitting.

A useful transfer test should vary the shape of ambiguity:

- Run terminal-state semantics;
- Job lifecycle/visibility semantics;
- temporal configuration semantics.

Three candidate tasks are therefore defined under `docs/benchmarks/candidates/`.

## Candidate scenario family

### RD-C1 Cancel Run

Primary ambiguity shape: terminal-state transition + alert/dashboard/idempotence interactions.

### RD-C2 Archive Job

Primary ambiguity shape: lifecycle visibility + scheduling/manual/in-progress/restore interactions.

### RD-C3 Retry Policy Update

Primary ambiguity shape: temporal configuration + existing/future Run boundary.

No exact oracle answers are frozen in this design phase.

## Design gate before any contestant run

Each scenario must pass all of:

1. implementation can remain synthetic and isolated;
2. at least four genuine product decisions exist that are not facts or reversible engineering choices;
3. evaluator can test each product decision through public/equivalent runtime seams;
4. public tests can validate plumbing without revealing the full oracle;
5. a reference solution can make the evaluator green;
6. at least one plausible wrong-but-reasonable implementation makes each hidden case red;
7. the scenario does not depend on production services, credentials or private data;
8. the task is not merely a renamed S02 pause/resume structure.

A scenario failing the gate is redesigned before any treatment outcome exists.

## Proposed economical execution strategy

Do not immediately run G0-G3 across all three scenarios.

After scenario/evaluator validation:

- select two scenarios with the strongest evaluator seams and most distinct ambiguity shapes;
- run a balanced one-shot screen: G0-G3 on each selected scenario, 8 contestant runs total;
- predeclare continuation thresholds before the first run;
- replicate only mechanisms that show a cross-scenario directional signal.

This design spends contestant capacity on transfer evidence rather than repeated S02 fitting.

## FIRST governance

FIRST-mode remains frozen.

External research may:
- falsify hypotheses;
- reveal portable principles;
- motivate FIRST-specific proposals.

It may not:
- automatically add a skill;
- automatically add a workflow;
- automatically revise FIRST-mode.

Any FIRST-facing design requires a separate proposal and explicit user agreement before implementation.


## Harness validation result

RD-C1 and RD-C2 passed the design gate with executable repository-native evidence.

GitHub Actions workflow run `39077925964` succeeded on research head `be2f1b4d608bac1b67257f5e6eb07c652c412702`.

The dedicated transfer-harness job verified:
- frozen-base red capability;
- reference-patch green paths;
- public regression preservation;
- eight targeted wrong-but-reasonable mutations rejected.

RD-C3 remains deferred because the existing frozen fixture intentionally carries the independent S04 retry-alert defect.

The next experiment should be a separately frozen, economical staged transfer screen. EXP-0016 itself contains no contestant outcome.
