# Legible Autonomy Research Framework

Status: ACTIVE RESEARCH PILLAR

## Core idea

FIRST wants agents that can work with very little operator intervention without becoming opaque black boxes.

The target is **legible autonomy**:

```text
high autonomy
+ strong external verification
+ persistent state
+ concise decision/evidence trace
+ selective escalation
= useful agent that the operator can trust and learn from
```

## Why model capability changes the workflow

Different models may need different amounts of procedural scaffolding.

A fixed workflow can underfit or overfit the model:

- too little structure can expose weak planning, poor recovery, or hallucinated completion;
- too much structure can waste a strong model's capability and create ceremony;
- strong implementation ability does not guarantee good epistemic calibration;
- strong reasoning does not eliminate the need for external verification.

Therefore the lab should measure **model × task × workflow** interactions, not assume one universal operating procedure.

## The key reliability problem

The hardest failure is not "the model knows it is uncertain."

It is:

> the model is missing an important consideration and does not realize that consideration exists.

Self-reported confidence cannot solve this by itself.

The system needs **structural uncertainty detectors**.

## Structural uncertainty detectors

A workflow should widen investigation or review when one of these conditions appears:

| Signal | Why it matters | Possible response |
| --- | --- | --- |
| No executable success predicate | completion can become a story instead of a fact | define oracle/test/repro first |
| Multiple plausible architectures | first idea may be locally convincing but globally weak | design twice / arena |
| Repeated failed fixes | shared premise may be wrong | attack the premise |
| Cannot reproduce bug | diagnosis lacks feedback loop | instrument or build harness |
| Cross-boundary change | hidden blast radius | architecture pass + integration checks |
| Conflicting evidence | mental model may be wrong | investigate disagreement |
| Unfamiliar external behavior | model prior may be stale or false | inspect docs/runtime |
| Large irreversible blast radius | cost of error is high | explicit approval + independent verifier |
| Implementer is sole verifier | correlated failure risk | independent review |
| Runtime differs from test surface | false-green risk | same-surface verification |

These triggers are useful even when the model itself reports high confidence.

## Decision authority model

A candidate FIRST policy:

```text
Question / ambiguity
        ↓
Can evidence answer it?
        ├─ yes -> agent investigates
        ↓
Is it a reversible engineering choice inside the granted goal?
        ├─ yes -> agent decides, records rationale, continues
        ↓
Does it change desired product behavior or preference?
        ├─ yes -> operator decides
        ↓
Is it irreversible, security-sensitive, or high-blast-radius?
        └─ yes -> approval gate
```

This preserves autonomy without treating product intent as an engineering fact.

## Seeing the work without becoming the bottleneck

The operator wants to learn from the agent's process. The research target is not a stream of every internal thought.

Instead, expose **meaningful engineering checkpoints**.

Recommended checkpoint schema:

```text
Goal
Evidence inspected
Current hypothesis or decision
Alternatives materially considered
Action taken
Artifact / commit / test
Verification result
Remaining uncertainty
Next step
```

A checkpoint should be short enough to skim and rich enough to teach.

For long autonomous runs, the agent continues after writing the checkpoint unless a real gate is reached.

## Two kinds of transparency

### Audit transparency

Purpose: detect mistakes and prove claims.

Artifacts:

- tests;
- logs;
- screenshots;
- traces;
- commit SHAs;
- PRs;
- decision records;
- runtime probes.

### Learning transparency

Purpose: help the operator understand methods and tradeoffs.

Artifacts:

- short rationale;
- alternative considered;
- why one approach was selected;
- why a hypothesis was rejected;
- what evidence changed the direction;
- what general lesson may transfer to future work.

Both can use the same checkpoint stream.

## Suggested operating modes to test

These are experiment treatments, not production decisions.

### Mode A: Opaque autonomy

Agent receives the task and returns only the final result.

Useful as a baseline because it maximizes interaction efficiency but minimizes learning and auditability.

### Mode B: Approval-heavy execution

Agent pauses at major decisions.

Useful as a contrasting baseline but likely expensive for the operator.

### Mode C: Legible autonomy

Agent records meaningful checkpoints and evidence while continuing automatically.

Pause only for genuine product/preference decisions, irreversible actions, security gates, or true blockers.

This is the leading FIRST hypothesis.

### Mode D: Adaptive legible autonomy

Mode C plus model/task calibration.

The amount of planning, alternative generation, decomposition, and review changes based on measured capability and risk.

This is the longer-term target.

## Model calibration

Do not infer capability only from brand or benchmark reputation.

Maintain empirical profiles by task class, for example:

| Task class | What to calibrate |
| --- | --- |
| Requirement discovery | unnecessary questions, silent assumptions, missed decisions |
| Architecture | rework, reviewer findings, alternative quality |
| Debugging | time to red signal, root-cause accuracy, speculative fixes |
| Implementation | acceptance rate, diff discipline, regression rate |
| Verification | false-green rate |
| Handoff | resume accuracy, repeated work |
| Autonomy | interruption count, premature stops, unsafe assumptions |
| Orchestration | duplicate work, conflicts, coordination overhead |

A model can be strong in one class and weak in another.

## Skill implications

Skills should increasingly encode:

- when extra structure is required;
- when the model may proceed directly;
- what evidence must exist;
- when independent review is mandatory;
- what state must persist;
- what checkpoint should be emitted for operator learning.

The long-term skill format may therefore include both a **procedure** and an **adaptation policy**.

Example conceptual shape:

```yaml
trigger: hard-debugging
required:
  - red-capable-feedback-loop
verification:
  - original-surface-repro
adaptation:
  low_calibration:
    - ranked-hypotheses
    - independent-review
  high_calibration:
    - ranked-hypotheses-if-stalled
checkpoint:
  - evidence
  - decision
  - verifier-result
```

The syntax is illustrative only. The research target is the concept.

## Research questions

1. How much scaffolding can be removed as model capability improves without increasing false greens or rework?
2. Which structural uncertainty detectors catch failures that model self-confidence misses?
3. Does legible autonomy materially improve operator learning without meaningfully slowing execution?
4. Which checkpoint information is actually useful to the operator?
5. When does alternative generation find better designs, and when is it pure overhead?
6. Should verification strictness remain constant as implementation capability rises?
7. Can the same skill expose different procedures according to model calibration while preserving one behavioral contract?

## Candidate benchmark extensions

Add a model-capability axis to selected RelayBoard scenarios.

For S01, test whether heavy scaffolding hurts strong models on tiny work.

For S02, test whether different models correctly classify fact vs reversible choice vs product decision.

For S04, test whether strong models still benefit from mandatory feedback-loop construction.

For S05, test whether model strength reduces or fails to reduce false-green completion.

For S06, compare resume performance when the prior agent is weak vs strong but the durable state is identical.

## Working thesis

The future is probably not "more autonomy means less visibility."

A better target is:

> stronger agents do more work independently, while producing better evidence and better compressed explanations of what mattered.

That gives the operator leverage without forcing the operator to stop learning.
