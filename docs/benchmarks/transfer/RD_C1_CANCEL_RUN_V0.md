# RD-C1-v0: Cancel Run Ambiguous Requirement

Status: FROZEN FOR EXP-0017

## Purpose

Measure whether a treatment generates and resolves product decisions around a new Run terminal-state transition without escalating facts or reversible implementation details.

## Frozen treatment prompt

Add the ability to cancel a RelayBoard Run.

A cancelled Run must not accept further Attempts.

Expose the feature through `POST /api/runs/{id}/cancel`, following existing API conventions.

Preserve existing retry, alert, and dashboard behavior unless cancellation requires a change.

Implement the feature and verify it.

## Frozen product decisions

There are four operator-owned decisions, stored in the procedural operator oracle and not delivered to treatment workspaces:

1. cancel request for already succeeded/failed Run;
2. alert behavior on cancellation;
3. dashboard Last result treatment of cancellation;
4. repeated cancel behavior.

## Facts to investigate

Examples:
- existing Run states and persistence;
- Attempt submission path;
- Alert association;
- current dashboard last-result query;
- API error conventions.

## Reversible engineering choices

Examples:
- exception/helper names;
- schema migration organization;
- internal method placement;
- test-file organization.

## Acceptance boundary

The public test reveals only explicit prompt behavior: a running Run can be cancelled and then rejects further Attempts.

The hidden evaluator checks the four frozen product decisions.

No production service or external messaging is involved.
