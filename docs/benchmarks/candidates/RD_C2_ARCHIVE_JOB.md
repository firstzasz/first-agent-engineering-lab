# RD-C2 Candidate: Archive Job

Status: CANDIDATE DESIGN; no oracle frozen; not runnable

## Goal

Test requirement discovery around lifecycle visibility and operational availability.

## Candidate treatment prompt

> Add the ability to archive and restore a RelayBoard Job.
>
> Archived Jobs should be hidden from the normal Jobs dashboard and normal Jobs listing.
>
> Preserve Run history and existing behavior unless archiving requires a change.
>
> Expose `POST /api/jobs/{id}/archive` and `POST /api/jobs/{id}/restore`.
>
> Implement the feature and verify it.

## Genuine product-decision candidates

The final oracle must resolve independently observable semantics such as:

1. Can an archived Job start new scheduled Runs?
2. Can an operator manually start a Run for an archived Job by id?
3. What happens to a Run already in progress when its Job is archived?
4. On restore, does the Job recover its pre-archive enabled/disabled state or return in a fixed state?

The prompt already fixes ordinary dashboard/list visibility and historical preservation. Those are not ambiguities.

## Facts/reversible choices treatments should not escalate

- current enabled/disabled semantics discoverable from code/tests;
- persistence implementation;
- HTML column/row mechanics needed to hide archived Jobs;
- migration/helper naming.

## Evaluator feasibility

Potential runtime checks:

- GET jobs/dashboard before and after archive/restore;
- scheduled/manual run APIs while archived;
- complete Attempts for a Run started before archive;
- restore both an originally enabled and originally disabled Job;
- verify historical Runs/last-result data remain durable.

## Difference from S02

Archive changes object lifecycle and discoverability. Although it interacts with scheduling/manual execution, the primary product boundary is hidden-but-addressable lifecycle semantics and state restoration, not temporary pause timing.
