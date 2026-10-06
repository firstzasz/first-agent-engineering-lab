# ADR-0001: Optimize for contextual fit, not a universal methodology winner

Status: Accepted for research methodology

Date: 2026-10-06

## Context

Agent-engineering methods can be strong in different classes of work. A workflow that performs well on long autonomous execution may be wasteful for a tiny fix. A method that excels at requirement discovery may require more operator interaction than another workflow. Host/runtime capabilities can also change the result.

The lab therefore should not ask only "Which methodology is best?" That question compresses away the context we actually care about.

FIRST also has an operator-style constraint: a technically strong method can still be a poor fit if it creates excessive interruption, ceremony, handholding, or workflow friction.

## Decision

Evaluate techniques by **scenario and operator fit**, and allow evidence-supported hybrids.

Research will:

1. compare methods across multiple task classes rather than a single fixture result;
2. keep the underlying synthetic system stable where practical, but vary scenarios such as ambiguous requirements, architecture, debugging, small changes, long autonomous work, session pickup, and parallel task graphs;
3. report strengths, weaknesses, costs, and host assumptions per scenario rather than producing one universal leaderboard;
4. include **operator fit** as an explicit evaluation dimension;
5. treat hybridization as a valid research outcome when experiments show complementary strengths;
6. prefer the smallest amount of process that improves measured outcomes for the task at hand.

## Operator-fit dimensions

Operator fit should measure at least:

- unnecessary questions and interruptions;
- ability to continue safely on reversible work;
- amount of ceremony relative to task size;
- quality of persistent GitHub state;
- ease of reviewing decisions and evidence;
- recoverability after interruption or failure;
- ability to adapt the workflow without fighting the operator's preferred working style.

These are not substitutes for correctness or safety. A workflow that feels convenient but produces weaker evidence or unsafe assumptions does not pass merely because it has low friction.

## Consequences

There may be no single winning methodology.

The likely output of the lab is a **context-sensitive playbook or router** that chooses lightweight or rigorous patterns according to task characteristics.

A future FIRST-oriented workflow may legitimately combine patterns from multiple sources, provided each adopted element is supported by evidence and passes the normal research-to-production gate.

## Non-goals

This ADR does not select pstack, Matt Pocock skills, or any future hybrid for production.

It does not assume the operator's preferences are universally optimal. They are one part of fitness for FIRST workflows and must be balanced against correctness, verification strength, safety, and maintainability.
