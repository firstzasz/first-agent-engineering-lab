# Requirement Discovery Mechanism Model v1

Status: RESEARCH MODEL; not a FIRST operating-mode specification

Date: 2026-10-18

## Why this model exists

Two Matt-port S02 runs surfaced all four frozen product decisions. EXP-0014 then isolated authority classification and a simplified decision frontier, but M0/M1/M2/M3 all surfaced only 2/4.

The simplest interpretation is that requirement discovery contains more than "know who to ask" and "traverse a frontier."

## Five functions

### D1 — Decision-space generation

Generate candidate externally visible behavior decisions before asking anybody.

Useful probes include:

- actors or invocation sources;
- object lifecycle states;
- events and transitions;
- before / during / after timing;
- success / failure / retry paths;
- current / future / already-in-progress work;
- repeated/idempotent requests;
- interactions with existing public surfaces;
- persistence/restart boundaries when relevant.

Output: a candidate behavior matrix, not answers.

### D2 — Dependency representation

Represent how unresolved decisions depend on one another.

A decision may be askable now, or may depend on another unresolved decision. Representation may be a tree, DAG, or compact dependency list. The representation is not itself a requirement source.

Output: candidate decisions plus prerequisite edges.

### D3 — Authority resolution

For every candidate uncertainty, determine who/what should resolve it:

- workspace evidence / fact lookup;
- reversible engineering judgment;
- operator-owned product/preference decision;
- irreversible/security gate;
- true blocker.

Output: an authority label with evidence where applicable.

### D4 — Question scheduling

Ask only operator-owned decisions whose prerequisites are resolved. Group related questions when that does not hide distinct semantics.

Output: operator exchanges with minimal unnecessary burden.

### D5 — Exhaustion / closure

After every material answer or discovery:

1. recompute unresolved decisions;
2. compare against the original behavior matrix and changed public surfaces;
3. verify no candidate branch disappeared merely because it was forgotten;
4. restate resolved product semantics when useful;
5. stop only when unresolved operator-owned behavior is empty.

Output: a closure record that distinguishes "frontier currently empty" from "decision space exhaustively covered."

## Important distinction

A frontier is a traversal primitive over a known decision set.

It cannot recover a decision that was never generated.

Therefore:

`empty frontier != complete requirement discovery`

unless an independent coverage/exhaustion mechanism establishes that the decision space itself was sufficiently generated.

## Candidate experimental mechanisms

These are vendor-neutral research probes, not FIRST features.

### G0 — Neutral

Normal host behavior.

### G1 — Behavior Matrix Generation

Before implementation:

1. identify changed entities, actors/invocation sources, lifecycle states, triggering events and public surfaces;
2. enumerate materially distinct before/during/after and source/state combinations;
3. mark cells whose externally visible behavior is not determined by supplied evidence;
4. classify fact/reversible cells yourself;
5. ask operator only unresolved product cells.

No dependency tree or frontier algorithm is mandated.

### G2 — Dependency Tree Generation

Before implementation:

1. state the top-level externally visible behavior being changed;
2. decompose it into concrete decision branches until each leaf can be resolved from evidence, engineering judgment, or an operator answer;
3. record dependencies between leaves;
4. ask currently unblocked operator-owned leaves;
5. recompute until every branch is closed.

No explicit actor/state/time matrix is mandated.

### G3 — Coverage Loop

Combine:

1. G1 behavior-matrix generation;
2. G2 dependency representation;
3. authority resolution;
4. frontier-style question scheduling;
5. final exhaustion check back against the original behavior matrix and changed public surfaces.

G3 is deliberately more complete and therefore carries more process overhead. The experiment must measure whether the extra ceremony buys materially better discovery.

## What this does not claim

- Matt's workflow is not reduced to these five functions.
- G1/G2/G3 are not copied Matt skills.
- A positive result would not prove causality outside the tested task family.
- No mechanism is part of FIRST-mode unless separately designed and explicitly approved.
