# RD-C1 Candidate: Cancel Run

Status: CANDIDATE DESIGN; no oracle frozen; not runnable

## Goal

Test whether a treatment discovers product semantics around introducing a new terminal-state transition.

## Candidate treatment prompt

> Add the ability to cancel a RelayBoard Run.
>
> A cancelled Run must not accept further Attempts.
>
> Expose the feature through `POST /api/runs/{id}/cancel`, following existing API conventions.
>
> Preserve existing retry, alert, and dashboard behavior unless cancellation requires a change.
>
> Implement the feature and verify it.

## Genuine product-decision candidates

The final oracle must resolve at least these independently observable semantics:

1. What should happen when cancel is requested for a Run that already succeeded or failed?
2. Does cancelling a running Run emit a failure Alert, a distinct cancellation Alert, or no Alert?
3. Does a cancelled Run become the Job's dashboard "Last result", or is cancellation excluded from that summary?
4. Is repeating cancel on an already-cancelled Run idempotent success or a conflict/error?

The statement "cancelled Runs must not accept further Attempts" is explicit in the prompt and is **not** an ambiguity.

## Facts/reversible choices treatments should not escalate

- where Run status is stored;
- how Attempt submission is routed;
- endpoint helper naming;
- test file organization;
- internal exception class names;
- schema migration organization.

## Evaluator feasibility

Potential black-box checks:

- create running Run -> cancel -> Attempt submission rejected;
- create terminal succeeded/failed Run -> cancel request;
- inspect Alerts after cancellation;
- inspect Dashboard after a previous completed result followed by cancellation;
- repeat cancel request.

## Difference from S02

This scenario changes a Run's terminal-state model rather than introducing a Job scheduling gate. It does not contain scheduled-miss/catch-up semantics.
