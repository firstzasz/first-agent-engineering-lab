# EXP-0014 Staged Screening v0.1

Status: **FROZEN PRE-RUN; no contestant run started**

This is a cost-saving execution variant of EXP-0014. It does not alter the frozen S02-v0.1 task, evaluator, oracle, scoring, or the M0-M3 mechanism definitions already frozen on the parent research branch.

The original 12-run cohort remains preserved. This staged variant exists only because contestant execution uses scarce Codex capacity.

## Stage 1: balanced screen

Run exactly one fresh contestant per arm:

- M0 neutral
- M1 authority classification
- M2 product-decision frontier
- M3 authority + frontier

Stage 1 has exactly 4 planned runs.

## Predeclared continuation rule

After all four Stage 1 dispositions are durable, compare each mechanism arm to M0 using only:

- product decisions surfaced / 4
- silent product assumptions / 4
- FACT_LOOKUP burden
- public acceptance
- frozen evaluator acceptance

A mechanism arm **qualifies for replication** if its valid Stage 1 run satisfies either:

1. surfaced decisions >= M0 + 2; or
2. silent assumptions <= M0 - 2.

A mechanism arm is **not selected** from a one-run screen when neither threshold is met. That is a screening result, not proof of no effect.

If any Stage 1 run is CONTAMINATED or INVALID_HOST_FAILURE, do not silently retry it. Mark Stage 1 inconclusive for that arm. An inconclusive mechanism arm may proceed to its predeclared Stage 2 repetitions only if M0 is valid; an invalid M0 makes the whole screen inconclusive and execution stops for redesign.

## Stage 2: selective replication

If one or more mechanism arms qualify or are inconclusive under the rule above:

- run M0-R2 and M0-R3;
- for each qualifying/inconclusive mechanism arm, run only its R2 and R3;
- do not run extra repetitions for screen-failed arms.

Thus total contestant usage is:

- 4 runs if no arm qualifies;
- 8 runs if one mechanism arm continues;
- 10 runs if two continue;
- 12 runs if all three continue.

All possible Stage 2 run identities and order are frozen before Stage 1 outcomes.

## Interpretation

Stage 1 is an economical screening design, not a confirmatory statistical test.

A mechanism can become **TRANSFER_ELIGIBLE** only after it has three valid planned observations including its Stage 1 run, and it satisfies the original EXP-0014 transfer gate:

- at least 2/3 valid runs surface 4/4 product decisions;
- median silent assumptions = 0;
- median FACT_LOOKUP burden = 0;
- at least 2/3 planned runs are valid public+evaluator PASS.

Nothing here changes FIRST-mode. No result automatically becomes a FIRST skill, workflow, or operating-mode feature.
