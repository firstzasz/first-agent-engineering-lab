# Skill Engineering Research Thesis

Status: ACTIVE RESEARCH PILLAR

## Thesis

Reusable procedural knowledge is a durable layer of agent engineering.

Models may know concepts, but useful engineering agents also need reusable ways to act: how to discover requirements, diagnose failures, execute changes, preserve state, verify outcomes, and hand work to another agent or session.

The lab therefore studies **skill engineering** as a long-term discipline. Current formats such as `SKILL.md` are implementation details.

## Working model

```text
Model
  ↓
Context / Knowledge
  ↓
Skills / Procedures
  ↓
Tools / Actions
  ↓
State / Memory
  ↓
Verification
  ↓
Environment
```

This model is deliberately decomposed so experiments can ask where a behavior belongs.

### Example separation

A project fact such as "the primary CI architecture is ARM64" is state or project knowledge.

Knowing the architectural differences between ARM64 and AMD64 is general knowledge.

A reusable procedure such as "when changing a container build, build the primary architecture, run container QA, test compatibility, verify the produced artifact, and retain evidence" is a skill.

Docker, GitHub Actions, or GitHub APIs are tools.

A larger delivery flow that invokes architecture checks, build, QA, compatibility checks, release, and verification is a workflow.

## Why this matters

Agent hosts and model names change quickly. Engineering procedures such as reproducing before fixing, separating implementation from verification, persisting task state, recording architectural decisions, and proving deployed artifacts are likely to outlive specific products.

This makes procedural knowledge a candidate for organizational knowledge that can accumulate over years without retraining the underlying model.

## Skill anatomy framework

Every studied skill should be decomposed into:

| Part | Research question |
| --- | --- |
| Trigger | When should this procedure activate, and when should it stay dormant? |
| Context | What facts, files, decisions, or environmental signals does it require? |
| Procedure | What reusable reasoning or action sequence does it encode? |
| Tools | What executable capabilities does it depend on? |
| State | What progress or decisions must survive across steps or sessions? |
| Verification | What evidence demonstrates success or failure? |
| Output contract | What does the next agent, workflow, or human receive? |

Additional properties to record where relevant:

- invocation mode: explicit, implicit, event-driven, scheduled;
- host assumptions;
- failure and recovery behavior;
- operator interruption policy;
- composability with other skills;
- expected cost and ceremony;
- idempotency and retry safety;
- security boundary.

## From instruction to capability package

One research direction is the progression:

```text
prompt fragment
    ↓
reusable instruction
    ↓
skill / runbook
    ↓
skill + tools
    ↓
skill + tools + state
    ↓
skill + executable verification
    ↓
tested capability package
```

This progression is not assumed to be universally better. The lab should identify when each added layer pays for its complexity.

## Target outcome

The lab should eventually produce evidence-backed guidance for deciding:

> What should be a skill, what should be a tool, what should be memory or explicit state, what should be a workflow, and what should be enforced by code rather than entrusted to model instructions?

That guidance should be portable enough to survive changes in model, vendor, host, and packaging format.

See [ADR-0002](./adrs/0002-skill-engineering-as-portable-procedural-knowledge.md).
