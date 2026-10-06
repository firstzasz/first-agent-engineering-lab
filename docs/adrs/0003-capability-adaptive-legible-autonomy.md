# ADR-0003: Capability-adaptive, legible autonomy

Status: Accepted for research methodology

Date: 2026-10-06

## Context

A single fixed agent workflow is unlikely to be optimal across models with different capabilities.

A strong model may be able to safely resolve more reversible engineering decisions without operator involvement. A weaker or less well-calibrated model may need more explicit decomposition, checkpoints, review, or human input.

However, model confidence is not enough. An agent can fail to notice what it does not know, can select a locally-plausible but globally-worse approach, and can produce convincing self-reports that are not evidence.

At the same time, FIRST does not want autonomy to become opacity. The operator may deliberately want to observe how work progresses in order to learn from the agent, inspect tradeoffs, and improve their own engineering judgment.

## Decision

FIRST Agent Engineering Lab will study **capability-adaptive, legible autonomy**.

The workflow may vary by model capability, task characteristics, and available verification, but the evidence standard does not weaken for stronger models.

Autonomy should be calibrated using objective task signals rather than the model's self-reported confidence alone.

### Autonomy envelope

Before deciding how independently an agent should act, consider:

- model capability on the relevant task class;
- task reversibility;
- blast radius;
- availability and strength of executable verification;
- observability of the environment;
- requirement ambiguity;
- novelty of the problem;
- security and irreversibility;
- cost of a wrong decision;
- quality of persistent state and recovery mechanisms.

Stronger models may receive a wider autonomy envelope when the task is reversible and strongly verifiable.

High-stakes or weakly-observable work should narrow the autonomy envelope even for the strongest model.

## Unknown-unknown safeguards

Do not rely on an agent to simply "know when it does not know."

Use structural triggers that force additional scrutiny when uncertainty may be hidden.

Examples:

- no executable success predicate exists;
- observed behavior conflicts with the current mental model;
- two or more failed fixes share the same premise;
- an architectural choice has multiple plausible shapes;
- the change crosses subsystem boundaries;
- evidence is incomplete or contradictory;
- the agent cannot reproduce the reported problem;
- the task depends on unfamiliar external behavior;
- a change has a large or irreversible blast radius;
- a result is supported only by the implementing agent's own report.

These triggers may require exploration, prototype, design alternatives, independent review, additional instrumentation, or operator escalation.

## Legible autonomy

Autonomy does not mean hiding the work.

The lab should distinguish **private model reasoning** from **reviewable engineering rationale**.

The operator does not need a raw internal chain of thought. Instead, long or important runs should externalize concise, durable checkpoints such as:

- current goal and success predicate;
- what evidence was inspected;
- important hypotheses under test;
- decision made and why;
- alternatives materially considered;
- what was rejected and why;
- artifact or commit produced;
- verification result;
- remaining uncertainty;
- next planned step.

This is a reviewable engineering trace, not a transcript of hidden reasoning.

## Learning value

Legibility has a second purpose beyond oversight.

The operator should be able to learn from the agent's methods, tradeoffs, experiments, and verification techniques without becoming a blocking approval gate.

A useful workflow can therefore be:

```text
agent acts autonomously
        +
records meaningful checkpoints
        +
links evidence
        +
continues unless a real gate is reached
```

The human can inspect the trace asynchronously and learn from it without slowing the run.

## Capability-adaptive procedures

Skills and playbooks should not assume all models need identical scaffolding.

Candidate policy:

- weaker or unproven model on a task class -> tighter procedure, smaller steps, stronger external review;
- strong but uncalibrated model -> broad execution ability with aggressive verification and challenge steps;
- strong and empirically calibrated model -> lighter scaffolding on low-risk work;
- any model on irreversible/high-blast-radius work -> explicit gates and independent evidence.

The benchmark should measure whether removing scaffolding actually preserves outcomes before simplifying a workflow.

## Alternative-search policy

A model may not spontaneously discover a better approach.

The lab should therefore test structural mechanisms that create opportunities to notice better options:

- design-twice or small alternative generation;
- adversarial or independent review;
- prototypes for empirical forks;
- explicit premise challenge after repeated failures;
- retrospective comparison of chosen vs rejected approaches.

These mechanisms should be triggered selectively because always generating alternatives can create substantial overhead.

## Consequences

The desired end state is not maximum autonomy at any cost.

It is:

> maximum safe autonomy that remains externally verifiable, recoverable, and understandable enough for the operator to learn from.

This ADR also implies that benchmark results should be stratified by model and host. A procedure that helps a weaker model may be redundant for a stronger one, while a procedure that is safe for one model may be unreliable for another.

## Non-goals

This ADR does not authorize exposing or depending on private chain-of-thought.

It does not assume stronger models need fewer verification steps.

It does not define a permanent numeric autonomy score.

It does not authorize production changes.
