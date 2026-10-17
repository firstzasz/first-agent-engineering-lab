# EXP-0017: Decision-generation transfer screen

Date: 2026-10-18
Status: **FROZEN PRE-RUN; no contestant run started**

## Question

Do vendor-neutral decision-space generation mechanisms improve product-requirement discovery on a new ambiguity shape, and does any observed signal transfer to a second distinct scenario?

## Evidence basis

EXP-0014 showed no Stage-1 advantage for authority classification or simplified frontier traversal on S02.

EXP-0015 trace synthesis identified decision generation and dependency representation as plausible missing functions.

EXP-0016 produced a five-function discovery model and independently verified executable harnesses for two transfer scenarios:

- RD-C1 Cancel Run;
- RD-C2 Archive Job.

GitHub Actions run `39077925964` verified red/green paths and targeted mutation sensitivity before this cohort was frozen.

## Arms

- G0 Neutral
- G1 Behavior Matrix Generation
- G2 Dependency Decision Graph
- G3 Coverage Loop

These are research mechanisms, not Matt/pstack/FIRST treatments.

## Economical staged design

Stage 1 runs G0-G3 once each on RD-C1 in a deterministic frozen order.

If valid G0 is incomplete, a mechanism proceeds only when it clears the frozen discovery threshold in `COHORT.json`.

If G0 itself reaches the 4/4 ceiling, all valid arms proceed to RD-C2 because C1 cannot discriminate.

If no mechanism clears the threshold, execution stops after four contestants.

Stage 2, when authorized, runs only G0 plus selected mechanisms on RD-C2, preserving the pre-frozen relative order.

Maximum total contestant runs: 8.

## Interpretation boundary

A two-scenario screening signal may make a mechanism `REPLICATION_ELIGIBLE`.

It does not:
- prove causality;
- establish generality;
- create a skill;
- revise FIRST-mode;
- justify production adoption.

Any FIRST-facing change remains a separate user-approved design decision.
