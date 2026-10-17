# RD-C2-v0: Archive Job Ambiguous Requirement

Status: FROZEN FOR EXP-0017

## Purpose

Measure whether a treatment generates and resolves product decisions around Job lifecycle visibility and operational availability.

## Frozen treatment prompt

Add the ability to archive and restore a RelayBoard Job.

Archived Jobs should be hidden from the normal Jobs dashboard and normal Jobs listing.

Preserve Run history and existing behavior unless archiving requires a change.

Expose `POST /api/jobs/{id}/archive` and `POST /api/jobs/{id}/restore`.

Implement the feature and verify it.

## Frozen product decisions

There are four operator-owned decisions, stored in the procedural operator oracle and not delivered to treatment workspaces:

1. scheduled Runs while archived;
2. manual Runs while archived;
3. already-running Run behavior when archive occurs;
4. enabled/disabled state after restore.

## Facts to investigate

Examples:
- current enabled/disabled scheduling behavior;
- manual versus scheduled Run paths;
- Run/Attempt persistence;
- dashboard/list implementation;
- historical last-result behavior.

## Reversible engineering choices

Examples:
- archived flag storage;
- response JSON representation unless behaviorally material;
- helper names;
- migration/test organization.

## Acceptance boundary

The public feature test reveals only explicit prompt behavior: archive hides a Job from normal list/dashboard and restore reveals it again.

The hidden evaluator checks the four frozen product decisions.

No production system or private data is involved.
