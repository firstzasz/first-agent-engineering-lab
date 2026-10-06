# Neutral Pilot Execution Handoff

Status: READY FOR FRESH AGENT EXECUTION

Date: 2026-10-07

## Why a fresh agent is mandatory

The research session that built the benchmark has inspected evaluator-only material, including the S02 operator oracle, the S04 injected root cause, and reference solutions.

It therefore cannot serve as a valid neutral treatment.

The neutral arm must run in a fresh agent context that has not seen those materials or prior outcomes.

## Frozen pilot base

Pilot Start State v0.1:

`2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`

Harness verification:

- PR #9 merge: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`
- positive-path/red-path CI: run `37547999430`, PASS
- PR #10 merge: `d064d17952afaac61488cc4918385c3b36b58dd7`
- runner repin CI: run `37548342313`, PASS

## Prepared evaluator-blind branches

The following branches contain only the treatment workspace tree, task, public fixture, public tests, and experiment manifest:

| Run | Scenario | Branch | Prepared commit |
| --- | --- | --- | --- |
| N-S01-001 | S01-v0 | `treatment/neutral/N-S01-001` | `563952fab378eda87da696cda4df12fe5c9d4e5e` |
| N-S02-001 | S02-v0.1 | `treatment/neutral/N-S02-001` | `2fcdf1702b93bb2beb79add5dc57d8b82e3bda22` |
| N-S04-001 | S04-v0 | `treatment/neutral/N-S04-001` | `58e55eebad654c357934b93b639e6ba91f6d235d` |

The recursive tree of each prepared commit was inspected after creation. None contains `experiments/`, evaluator, oracle, or reference-solution paths.

## Fresh-agent instruction

The fresh neutral agent should receive only this operating instruction:

> Work only from the checked-out treatment branch. Read `TASK.md`, inspect the code and public tests, implement the task, and verify your work. Use ordinary host defaults. Do not fetch or inspect other branches, lab evaluator material, oracle files, reference solutions, or previous treatment outcomes.

Do not add pstack, Matt Pocock skills, FIRST-mode, or any special benchmark methodology to a neutral run.

## S02 operator behavior

S02 may legitimately require product decisions.

The fresh agent should ask normally when it believes operator input is required.

A separate evaluator/operator process must answer only valid product/preference questions from the frozen S02 answer sheet. It must not volunteer extra requirements.

The research session may serve as the evaluator/operator for S02 because the treatment agent itself remains fresh.

Every question and answer must be preserved in the run record.

## Completion handoff

At the end of a run, preserve:

- exact host and model;
- start and finish time if measurable;
- all operator questions;
- any visible checkpoints;
- agent completion claim;
- git diff and commits;
- public test output.

Then evaluate the finished branch/workspace from the lab side with the frozen evaluator.

Do not reveal evaluator failures to the same treatment agent and let it retry as part of the same run unless the experiment explicitly defines such a feedback condition.

## Contamination rule

Mark a run **CONTAMINATED** and exclude it from outcome comparison if the treatment agent:

- reads evaluator/oracle/reference-solution material;
- reads prior outcomes for the same scenario;
- receives hidden product answers before asking;
- starts from anything other than the frozen treatment branch;
- receives methodology instructions beyond neutral host defaults.

Preserve contaminated runs as evidence. Do not delete them.

## Current execution boundary

The lab infrastructure is ready.

Actual neutral execution now requires a genuinely fresh coding-agent context with write access to one prepared treatment branch.

This is an experimental-validity boundary, not a request for product or architecture approval.
