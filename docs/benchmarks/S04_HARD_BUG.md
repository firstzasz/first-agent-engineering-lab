# S04: Deterministic Hard Bug

Status: FROZEN FOR PILOT

Version: S04-v0

## Purpose

Measure debugging discipline, root-cause discovery, false-fix resistance, and same-surface verification.

## Frozen treatment prompt

> Some RelayBoard Jobs that use retries are sending the same failure alert twice for a single Run.
>
> Diagnose and fix the bug.
>
> Do not suppress legitimate failure alerts for distinct Runs.
>
> Preserve retry behavior and verify the fix.

The prompt intentionally names the symptom, not the root cause.

## Starting-state requirements

The fixture must contain a deterministic defect for which:

- the duplicate appears on a Run that reaches terminal failure after retry behavior;
- the notification/alert adapter itself is not the root cause;
- a naive deduplication patch in the adapter can hide the symptom while breaking a legitimate case;
- a tight local reproduction can be built or discovered.

## Public acceptance intent

Normal tests cover expected Run, retry, and alert behavior but do not fully expose the injected failing edge case.

## Evaluator oracle intent

The evaluator verifies:

- one failure Alert per terminally failed Run;
- two distinct failed Runs each produce their own Alert;
- retry Attempts remain part of one Run;
- retry count/behavior is unchanged;
- the fix addresses lifecycle ownership rather than globally suppressing duplicate-looking alerts;
- the original failing scenario passes after the fix.

The exact injected root cause is frozen in the evaluator root-cause oracle.

## Metrics of interest

- feedback loop built before fix;
- time/steps to first valid red signal;
- root cause correctly identified;
- speculative fixes;
- wrong files changed;
- regression test quality;
- original-surface verification;
- hidden regression result;
- cleanup of temporary instrumentation.

## False-fix trap

A treatment that simply deduplicates all alerts by message text or Job id should fail evaluator cases because distinct Runs are allowed to produce equivalent alerts.
