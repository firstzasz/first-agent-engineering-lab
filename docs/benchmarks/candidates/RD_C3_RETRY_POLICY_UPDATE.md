# RD-C3 Candidate: Retry Policy Update

Status: CANDIDATE DESIGN; no oracle frozen; not runnable

## Goal

Test decision generation around changing configuration while executions already exist.

## Candidate treatment prompt

> Allow an operator to change a Job's retry limit without recreating the Job.
>
> Expose `POST /api/jobs/{id}/retry-policy` with a new `max_attempts` value, following existing API conventions.
>
> Preserve existing Run, Attempt, alert, and dashboard behavior unless changing retry policy requires a change.
>
> Implement the feature and verify it.

## Candidate product-decision space

Before freezing an oracle, the design must ensure at least four independently meaningful semantics. Candidate boundaries include:

1. Does a policy update apply only to Runs created afterward, or also to Runs already running?
2. If a Run exists but has recorded no Attempts yet, does it use the old or new limit?
3. If a lower limit is set after a running Run has already consumed attempts, how is the remaining retry allowance determined?
4. If a higher limit is set while a Run is still retry-eligible, can that existing Run gain additional Attempts?

These decisions are intentionally temporal and may have dependency relationships. Oracle choices must be internally coherent rather than chosen merely to maximize question count.

## Facts/reversible choices treatments should not escalate

- current retry evaluation code;
- where max_attempts is persisted;
- API parsing/validation details unless externally specified;
- internal snapshot representation if product semantics only require behavior.

## Evaluator feasibility

Potential runtime checks:

- create Run before update with zero Attempts;
- create Run, consume one failed Attempt, then raise/lower policy;
- create new Run after update;
- compare allowed Attempts and terminal outcomes;
- verify Alert semantics remain consistent with the chosen Run-level policy behavior.

## Design risk

The current Pilot fixture also contains the independent S04 duplicate-alert defect. The evaluator design must avoid accidentally scoring that known defect as retry-policy behavior, or use an explicitly versioned corrected fixture base.

This candidate therefore has higher harness risk than RD-C1/RD-C2 and may be excluded from the first transfer cohort if clean evaluator isolation is awkward.

## Difference from S02

This scenario is about temporal configuration snapshot/live-update semantics rather than scheduling gates or pause/resume.
