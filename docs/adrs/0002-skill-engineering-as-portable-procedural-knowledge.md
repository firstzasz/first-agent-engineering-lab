# ADR-0002: Treat skill engineering as portable procedural knowledge

Status: Accepted for research methodology

Date: 2026-10-06

## Context

The lab is studying repositories that currently package reusable agent behavior as skills, playbooks, modes, commands, or related instruction artifacts.

The durable research target is not the current `SKILL.md` file format. Model vendors, agent hosts, plugin formats, and invocation syntax may change quickly.

The more durable question is how to encode reusable **procedural knowledge**: what an agent should do when a recognizable situation occurs, what context and tools it needs, what state must persist, and what evidence proves success.

A useful conceptual stack for this lab is:

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

These layers overlap in real systems, but separating them is useful for research.

## Decision

The lab will study **skill engineering**, not merely the syntax or catalog of today's skill files.

For research purposes:

- **Knowledge** primarily describes facts, concepts, constraints, and how the world or system works.
- **Memory / state** stores durable situation-specific facts, decisions, progress, and context needed later.
- **Skill / procedure** encodes reusable know-how for handling a class of situations.
- **Tool / action** gives the agent an executable capability against an environment.
- **Workflow** composes multiple skills, tools, states, and verification steps toward a larger outcome.
- **Verification** determines whether claimed outcomes are actually supported by evidence.
- **Environment** supplies the runtime, repository, services, policies, and other operational constraints in which the agent acts.

The boundaries are research hypotheses, not immutable ontology. Experiments may show that some concerns should move between layers.

## Skill anatomy

When analyzing or designing a reusable skill-like artifact, inspect at least:

1. **Trigger**  
   When should it run? When should it not run?

2. **Context**  
   What information must be available before it can act safely and effectively?

3. **Procedure**  
   What reusable decision process or sequence does it encode?

4. **Tools**  
   Which executable capabilities may or must it use?

5. **State**  
   What must persist during or after execution so another step, agent, or session can continue?

6. **Verification**  
   How does the system know the procedure succeeded? Which claims can be checked mechanically?

7. **Output contract**  
   What durable artifact, state transition, evidence, or handoff does the next consumer receive?

## Capability-package hypothesis

The lab will test the hypothesis that robust skills tend to evolve beyond prose instructions.

A mature capability may combine:

```text
instruction
+ executable helper
+ tests
+ fixtures
+ tool definitions
+ verification
```

For example, "verify deployment carefully" is weaker than a reusable verification capability with executable checks, fixtures, and tests.

This is a hypothesis to test, not an assumption that every skill should contain code.

## Long-term research questions

The lab should eventually be able to answer:

- What should be a skill rather than ordinary knowledge?
- What should be persisted as memory or explicit task state?
- What should be an executable tool instead of an instruction?
- What belongs in a larger workflow or playbook?
- What behavior should be enforced by code, tests, schemas, policies, or CI instead of trusting a model to remember prose?
- Which parts are portable across ChatGPT, Codex, Cursor, Claude Code, and future agent hosts?
- When does a reusable procedure create useful leverage, and when does it create unnecessary ceremony?

## Consequences

Research notes about pstack and Matt Pocock skills should extract principles and anatomy rather than merely inventory command names.

Future experiments may compare:

- prose-only skill vs executable capability package;
- verification described in instructions vs verification enforced by code;
- ephemeral context vs persistent task state;
- host-specific orchestration vs a portable procedure with host adapters;
- one large workflow vs composable small skills;
- automatic invocation vs explicit operator invocation.

The expected output of the lab is portable engineering knowledge and evidence-backed patterns, not dependence on one file format or one vendor.
