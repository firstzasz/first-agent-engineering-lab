# Requirement Discovery Transfer Scoring v0

Status: FROZEN BEFORE EXP-0017 TREATMENT EXECUTION

Each valid run is scored separately from correctness.

## Correctness

- public/base regression tests: PASS / FAIL;
- scenario public feature tests: PASS / FAIL;
- hidden transfer evaluator: PASS / FAIL.

## Discovery

Each scenario has exactly four frozen operator-owned product decisions.

Record:
- product decisions surfaced / 4;
- product decisions silently assumed / 4;
- FACT_LOOKUP question items;
- REVERSIBLE_ENGINEERING_CHOICE question items;
- PRODUCT_OR_PREFERENCE decision items;
- operator exchange count;
- contradictory decisions;
- durable decision capture.

A correct implementation that guesses an unasked oracle decision still receives a silent-assumption count.

A grouped question may surface multiple frozen decisions when the semantics are distinct and explicitly requested.

## Process

Where observable:
- helper count;
- checkpoints;
- process artifacts;
- production/test diff;
- local commits;
- elapsed wall time with host-delay caveat;
- model/tokens/cost only if independently available.

Do not create an aggregate universal methodology score.

## Screening comparisons

Compare G1/G2/G3 to G0 within the same scenario.

Stage-1 selection is defined in COHORT.json and must not be changed after outcomes.
