# S01: Tiny Reversible Change

Status: FROZEN FOR PILOT

Version: S01-v0

## Purpose

Measure whether an approach scales down gracefully or adds unnecessary ceremony to a tiny, low-risk, reversible task.

## Frozen treatment prompt

> On the RelayBoard dashboard, change the Jobs table column heading from **Last result** to **Latest result**.
>
> Do not change API behavior or unrelated dashboard behavior.
>
> Implement the change and verify it.

No additional product clarification is required.

## Starting-state assumptions

The frozen fixture must contain:

- a dashboard with a Jobs table;
- the exact visible heading `Last result`;
- an executable dashboard rendering test or equivalent acceptance path.

## Public acceptance intent

The normal fixture tests should be capable of proving:

- the dashboard renders `Latest result`;
- the old heading `Last result` is absent from the corresponding table heading;
- unrelated API tests remain green.

## Evaluator oracle intent

The evaluator checks:

- only the intended visible label changed;
- no API contract changed;
- no unrelated behavior was modified;
- the treatment did not introduce needless runtime dependencies or broad refactors.

## Metrics of interest

S01 uses the common scoring rubric with special attention to:

- artifacts created;
- subagents used;
- operator questions;
- tool/action count;
- diff size;
- verification level.

## Expected methodological pressure

A good workflow should recognize that heavy architecture, ticket graphs, multi-agent fan-out, and extensive specification are unlikely to earn their cost here.

This expectation is part of the benchmark design, not a guarantee that FIRST-mode wins.
