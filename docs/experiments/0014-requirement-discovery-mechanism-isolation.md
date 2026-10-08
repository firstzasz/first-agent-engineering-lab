# EXP-0014: Next Cohort Design — Requirement-Discovery Mechanism Isolation

Date: 2026-10-08
Status: PLANNED; no treatment run started

## Why not a full Round 3 yet

Two independent rounds now provide ten valid matched treatment/scenario pairs.

The repeated evidence is uneven by scenario:

- S01 repeatedly shows the same one-line application change and stable helper structure, while absolute process-artifact volume varies.
- S04 repeatedly converges on the same deterministic root cause and valid red/fix/green behavior for FIRST, Matt and Neutral. This fixture currently has limited discriminating power for methodology.
- S02 continues to distinguish requirement-discovery behavior:
  - Matt: 4/4 surfaced, 0 silent in both rounds.
  - FIRST: 3/4 then 2/4.
  - Neutral: 0/4 then 3/4.
  - pstack lacks a complete Round 2 pair because P-S02-002 was excluded for host failure.

A third full 4×3 replication would spend most runs re-measuring cells that currently add little causal information.

## Research question

Does an explicit, recomputed product-decision frontier materially improve complete requirement elicitation without importing the full ceremony of a larger workflow?

This question is motivated by the repeated Matt S02 result but is not yet causally established.

## Portable mechanisms to isolate

Separate principles from vendor/workflow packaging.

### M0 — Neutral control

Normal host behavior. No added requirement-discovery procedure.

### M1 — Authority classification only

Provide only a compact classifier:

- FACT: investigate from code/tests/docs.
- REVERSIBLE_ENGINEERING: agent decides and records if material.
- PRODUCT_OR_PREFERENCE: ask operator.
- IRREVERSIBLE_OR_SECURITY: gate.
- TRUE_BLOCKER: report.

No explicit decision frontier or grilling rounds.

### M2 — Decision frontier only

Provide only a compact requirement-discovery procedure:

1. list unresolved behavior decisions that affect externally visible semantics;
2. classify each as agent-answerable fact/engineering choice versus operator-owned product decision;
3. ask only operator-owned decisions;
4. after each answer, recompute the unresolved decision frontier;
5. stop asking when the frontier contains no unresolved operator-owned decision.

Do not add FIRST-mode, pstack, Matt ticketing/spec orchestration, multi-agent review, or unrelated ceremony.

### M3 — Authority classification + decision frontier

Combine M1 and M2, but no other FIRST/Matt workflow behavior.

### Reference comparators

Keep frozen FIRST-mode v0 and matt-codex-port-v0 available as system-level reference comparators, not as mechanism-pure arms.

## Pilot cohort

Before execution, freeze this cohort and its run order.

Recommended first cohort:

- scenario: existing S02-v0.1 only;
- mechanism arms: M0, M1, M2, M3;
- independent repetitions: 3 per arm;
- total: 12 fresh contestant runs;
- model request: GPT-6.1 Sol / High where supported;
- procedural isolation and evaluator protocol unchanged.

This cohort estimates stochastic stability on the existing S02 task. It does **not** establish transfer to other product-ambiguity tasks.

If M2/M3 show a repeated elicitation advantage, design a later transfer cohort with new frozen ambiguous-requirement scenarios before claiming generality.

## Primary outcomes

Predeclare per run:

- frozen product decisions surfaced / 4;
- silent assumptions / 4;
- FACT_LOOKUP questions;
- REVERSIBLE_ENGINEERING questions;
- operator exchanges;
- public acceptance;
- frozen evaluator acceptance.

Correctness does not erase silent assumptions.

## Secondary outcomes

Where observable:

- process/evidence footprint;
- helper count;
- visible checkpoints;
- candidate production/test diff;
- wall-clock observation with host-delay caveat.

Do not infer token/cost efficiency unless the host exposes trustworthy usage data.

## Success interpretation

A mechanism signal is supported only if repeated runs show a directional difference that is not explained solely by correctness luck or one anomalous run.

Examples:

- M2 > M0 on surfaced decisions with no increase in FACT questions suggests decision-frontier value.
- M3 > M2 suggests authority classification contributes beyond frontier recomputation.
- M1 ~= M0 but M2/M3 improve would argue the frontier mechanism is more important than classification alone.
- No stable separation means the Round 1/2 Matt result remains a system-level observation rather than a portable causal mechanism.

Do not tune mechanisms after seeing within-cohort outcomes.

## What remains frozen

This experiment does not modify:

- Pilot Start State v0.1;
- S02-v0.1 prompt;
- S02 operator oracle;
- scoring rubric;
- evaluator;
- FIRST_MODE_V0.md;
- Round 1 or Round 2 evidence;
- pstack/Matt frozen Codex ports.

New mechanism-arm instructions must be frozen before the first run.

## Limitations

Three repeats per arm remain small-sample exploratory evidence.

The same S02 task can measure stochastic repeatability but not task-family generalization.

Procedural isolation, missing runtime identity attestation and incomplete raw host traces remain inherited limitations.

## Recommendation

Freeze M0–M3 treatment packets and run this 12-run mechanism cohort before spending another full 12-run system-level replication.

If the decision-frontier mechanism replicates, then design multiple new ambiguous-requirement scenarios to test transfer.

No production adoption follows from this experiment without a separate proposal/ADR and FIRST architecture review.
