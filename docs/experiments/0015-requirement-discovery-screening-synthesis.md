# EXP-0015: Requirement-discovery screening synthesis

Date: 2026-10-18
Status: ANALYSIS ONLY; no new contestant run started

## Trigger

EXP-0014 staged screening completed four valid Stage 1 runs, one each for M0 neutral, M1 authority classification, M2 decision frontier, and M3 authority + frontier.

All four passed public tests and the unchanged frozen evaluator.

All four surfaced 2/4 frozen S02 product decisions and silently assumed 2/4. All four incurred one FACT_LOOKUP burden. No mechanism met the predeclared continuation threshold, so Stage 2 correctly stopped.

This does **not** prove M1-M3 ineffective.

## Key observation

The four Stage 1 operator exchanges converged on the same two product decisions:

- manual run while paused;
- in-progress run behavior.

None surfaced:

- what happens to a scheduled start that occurs while paused;
- whether resume catches up missed scheduled work or only permits future schedule times.

The simplified M2/M3 frontier instructions therefore did not reproduce the 4/4 elicitation observed in both frozen Matt-port S02 runs.

## Trace comparison with Matt S02

Matt S02 Round 1 explicitly invoked `grill-with-docs`, which composes `grilling` and `domain-modeling`.

The frozen Matt port requires, before frontier questioning:

- read the task, glossary, relevant code and tests;
- map decisions as a **dependency tree**;
- use domain modeling to challenge terms and invent concrete edge-case scenarios;
- cross-reference claimed behavior with code;
- then ask the currently answerable product/preference frontier;
- recompute until the tree is exhausted;
- confirm shared understanding before implementation.

In Round 1, Matt's first question explicitly decomposed execution into scheduled, manual and existing-run attempts, surfacing three frozen decisions, then separately asked resume catch-up.

In Round 2, Matt again decomposed pause scope into scheduled/manual/in-progress behavior. A later recomputed-frontier confirmation explicitly surfaced no-catch-up before implementation.

By contrast, the EXP-0014 M2 instruction began with "write down currently unresolved externally visible behavior decisions" and then operated a frontier over that set. It did not prescribe a strong mechanism for **generating a complete candidate decision set**.

## Mechanism hypothesis

The repeated Matt result may depend on a pipeline with at least five separable functions:

1. **Decision generation**  
   Derive candidate product decisions from domain concepts, state transitions, actors/events, edge cases and code seams.

2. **Dependency representation**  
   Organize candidate decisions as a design/dependency tree so downstream decisions are not forgotten.

3. **Authority resolution**  
   Distinguish facts and reversible engineering choices from operator-owned product decisions.

4. **Frontier traversal**  
   Ask only currently answerable operator-owned decisions.

5. **Exhaustion check / shared-understanding confirmation**  
   Recompute after answers and do not act until no unresolved branch remains.

EXP-0014 isolated authority classification and a simplified frontier, but did not independently isolate decision generation or dependency-tree construction.

Therefore the screening result weakens the hypothesis:

> "decision frontier alone explains Matt's S02 advantage"

It does **not** weaken the broader hypothesis:

> "structured discovery that first generates a complete decision space, then traverses it, improves requirement elicitation."

## Important conceptual distinction

A frontier is primarily a **selection/traversal mechanism**.

It cannot ask about a decision that was never generated.

This distinction explains how an agent can truthfully report "frontier empty" while still leaving product assumptions undiscovered.

## Next research step

Do not run the stopped EXP-0014 Stage 2.

Before another contestant cohort, perform a small static mechanism design exercise focused on decision-space generation.

Candidate mechanism families for a future frozen cohort:

- neutral control;
- **scenario/state-transition enumeration only**;
- **dependency/design-tree construction only**;
- **scenario generation + design tree + frontier**.

These should remain vendor-neutral research mechanisms. Matt's upstream implementation is evidence and inspiration, not a component to copy into FIRST.

A new cohort should use either:
- a fresh ambiguous-requirement task family, or
- multiple new tasks, to avoid repeatedly fitting mechanisms to S02.

## FIRST governance

No EXP-0014/0015 result modifies FIRST-mode.

Even if a future mechanism repeatedly succeeds, it becomes only an evidence-backed candidate. A separate FIRST-specific design requires explicit user approval before any FIRST-mode version changes.

## Current conclusion

IMPLEMENTED:
- staged four-arm screening;
- durable 4/4 dispositions;
- predeclared screen stop;
- trace comparison against both Matt S02 runs.

VERIFIED:
- all four Stage 1 runs passed public + frozen evaluator;
- all four scored 2/4 surfaced, 2/4 silent;
- Matt S02 scored 4/4 in both earlier rounds;
- Matt traces explicitly used grill/domain-modeling plus decision-tree/frontier behavior.

HYPOTHESIS:
- decision-space generation and dependency representation, not frontier traversal alone, may be the missing causal mechanism.

NOT PROVEN:
- that domain modeling is sufficient;
- that design-tree construction is sufficient;
- that the full Matt workflow is necessary;
- that any discovered mechanism belongs in FIRST-mode.
