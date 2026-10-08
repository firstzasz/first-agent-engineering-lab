# Requirement-Discovery Mechanism Cohort v0

Status: **FROZEN PRE-RUN DESIGN; no contestant run started**

Experiment: EXP-0014

Purpose: isolate small, portable requirement-discovery mechanisms without treating pstack, Matt skills, or FIRST-mode as indivisible winners.

This cohort is intentionally **not a FIRST-mode revision**. No mechanism discovered here is adopted into FIRST-mode automatically. Any FIRST-specific adoption requires a separate proposal, explicit user approval, and a separately versioned experiment.

## Cohort

- Scenario: S02-v0.1 only
- Frozen start: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`
- Arms: M0, M1, M2, M3
- Repetitions: 3 independent fresh-context runs per arm
- Total planned runs: 12
- Model request: GPT-6.1 Sol / High where supported
- Evaluator protocol: unchanged Evaluator Protocol v0
- No outcome-dependent retry or treatment tuning

The S02 task prompt is copied byte-for-content from the frozen treatment prompt only. Known ambiguity classes, operator oracle, evaluator implementation and reference solutions are not included in contestant packets.

## Arms

- **M0 Neutral**: normal host behavior; no additional mechanism instruction is delivered.
- **M1 Authority classification**: explicit uncertainty/decision authority taxonomy only.
- **M2 Decision frontier**: maintain and recompute unresolved operator-owned product decisions, without the full authority taxonomy.
- **M3 Authority + frontier**: combine M1 and M2.

These are mechanism probes, not vendor-branded workflows.

## Primary outcomes

Per valid run:

- product decisions surfaced / 4;
- silent product assumptions / 4;
- FACT_LOOKUP questions;
- REVERSIBLE_ENGINEERING_CHOICE questions;
- PRODUCT_OR_PREFERENCE_DECISION exchanges;
- public acceptance;
- frozen evaluator acceptance.

Correct implementation does not erase silent assumptions.

## Transfer gate

A mechanism becomes **eligible for a separate transfer experiment**, not for FIRST adoption, when all of the following hold in this cohort:

1. at least 2 of 3 valid runs surface all 4 frozen product decisions;
2. median silent assumptions across valid runs is 0;
3. median FACT_LOOKUP burden is 0;
4. at least 2 of 3 planned runs produce valid public+evaluator PASS outcomes, excluding protocol-invalid/host-failure runs rather than silently replacing them.

For a stronger comparative signal against M0, also report whether the mechanism improves median surfaced decisions by at least 2 and reduces median silent assumptions by at least 2. These thresholds are exploratory and frozen before outcomes.

Passing this gate means only “worth testing on new ambiguous-requirement tasks.”

## Guardrails

- Do not modify Pilot Start State v0.1, S02-v0.1, oracle, scoring or evaluator.
- Do not modify FIRST_MODE_V0.md.
- Do not import Matt/pstack bundles into contestant packets.
- Do not call M1/M2/M3 “FIRST”.
- Do not tune an arm after observing any cohort outcome.
- If contamination or unrecoverable host failure occurs, preserve/exclude it and do not silently retry.
- Hidden evaluation occurs only after contestant/helper contexts terminate.
- Nothing merges to main.

See `COHORT.json`, `EXECUTION_ORDER.json`, `TASK_S02_V0_1.md`, and `methods/`.
