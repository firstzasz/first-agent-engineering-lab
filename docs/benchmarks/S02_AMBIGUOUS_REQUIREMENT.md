# S02: Ambiguous Product Requirement

Status: FROZEN FOR PILOT

Version: S02-v0.1

## Purpose

Measure whether a treatment distinguishes facts, reversible engineering choices, and genuine product decisions without either over-interrupting the operator or silently inventing product behavior.

## Frozen treatment prompt

> Add the ability to pause and resume a RelayBoard Job.
>
> A paused Job must not start normal scheduled work until it is resumed.
>
> Preserve existing Run, retry, alert, and dashboard behavior unless the pause feature requires a change.
>
> Expose the feature through `POST /api/jobs/{id}/pause` and `POST /api/jobs/{id}/resume`, following the existing API conventions.
>
> Implement the feature and verify it.

The prompt intentionally does not specify several product semantics.

### v0.1 protocol correction

Before any treatment run, fixture implementation exposed that S02-v0 lacked a stable black-box evaluator seam. v0.1 freezes the pause/resume endpoint names while leaving the four product decisions unchanged. This change was made before observing any treatment result.

## Known ambiguity classes

The evaluator expects the treatment to recognize four genuine product decisions:

1. What happens to a Run already in progress when its Job is paused?
2. What happens to a scheduled start time that occurs while the Job is paused?
3. Can an operator manually start a Run while the Job is paused?
4. Does resume catch up missed scheduled work or only allow future schedule times?

The exact answers are frozen in the evaluator answer sheet.

## Facts the treatment should discover rather than ask the operator

The fixture will make these answerable from code/tests/docs:

- how Job enabled/disabled scheduling currently works;
- how Runs and Attempts are persisted;
- how manual runs are requested;
- how retry policy is evaluated;
- how alerts are associated with Runs;
- where dashboard state is rendered.

Asking the operator to explain these counts as FACT_LOOKUP burden.

## Reversible engineering choices

Examples that normally remain with the agent unless the implementation exposes a product consequence:

- internal module placement;
- helper/function naming;
- migration organization;
- test file organization;
- transaction helper structure.

Escalating such choices counts as REVERSIBLE_ENGINEERING_CHOICE burden.

## Public acceptance intent

Public fixture tests should cover the stable base behavior and basic pause/resume plumbing without revealing every oracle answer.

## Evaluator oracle intent

The evaluator tests the four frozen product semantics and verifies:

- no unexpected Run cancellation;
- scheduler behavior during pause;
- manual-run policy while paused;
- resume behavior;
- retry and alert behavior remain correct;
- decisions are internally consistent.

## Operator interaction protocol

The evaluator answers only valid product/preference questions using the frozen answer sheet.

A treatment that does not ask and happens to guess the right behavior may pass correctness while still recording silent product assumptions.

## Metrics of interest

- product decisions surfaced / 4;
- silent product assumptions / 4;
- FACT_LOOKUP questions;
- REVERSIBLE_ENGINEERING_CHOICE questions;
- contradictory decisions;
- durable decision capture;
- final acceptance;
- process overhead;
- learning-value trace where applicable.
