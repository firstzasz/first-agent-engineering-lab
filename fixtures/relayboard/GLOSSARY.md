# RelayBoard Domain Glossary

Status: FROZEN FOR PILOT

Date frozen: 2026-10-06

This glossary defines the base domain shared by S01, S02, and S04.

It intentionally does **not** define the semantics of pausing a Job. Those semantics are the ambiguity under test in S02.

## Job

A configured unit of work that may produce Runs.

A Job has:

- a stable id;
- a display name;
- an enabled/disabled scheduling state;
- a retry policy;
- zero or more alert rules.

## Run

One execution of a Job.

A Run has a stable id and one terminal outcome:

- succeeded;
- failed.

A Run may contain one or more Attempts.

## Attempt

One try within a Run.

The first try is attempt 1.

A failed Attempt may produce another Attempt when the Job's RetryPolicy permits it.

Attempts are not separate Runs.

## RetryPolicy

Rules that determine the maximum number of Attempts for a Run.

For the pilot fixture, retry behavior must be deterministic.

A retry does not create a new Run id.

## AlertRule

A rule that can emit an Alert after a Run reaches a terminal outcome.

For the pilot, the relevant rule is a failure alert.

The alert is associated with the Run, not with an individual Attempt.

## Alert

A synthetic notification emitted by an AlertRule.

No real external messaging service is used.

Each Alert records enough synthetic data for tests to determine which Run caused it.

## Dashboard

A minimal operator-facing view of Jobs and recent Runs.

The Dashboard exists partly to provide a real user-facing surface for tiny-change and later verification experiments.

## Scheduler

The component that determines whether a scheduled Job should start a new Run.

Its exact implementation is fixture detail, not a domain term.

## Manual run

A Run explicitly requested by an operator/API call rather than started by the scheduler.

## Pause

Not defined in the base glossary.

S02 intentionally asks the treatment to introduce pause behavior while several product semantics remain unresolved.
