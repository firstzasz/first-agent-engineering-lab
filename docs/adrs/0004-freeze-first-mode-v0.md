# ADR-0004: Freeze FIRST-mode v0 as an experimental treatment

Status: Accepted for research methodology

Date: 2026-10-06

## Context

The lab now has three substantive approach families to compare:

- Lauren Tan / pstack;
- Matt Pocock / skills;
- a FIRST-specific operating hypothesis emerging from the lab's goals around autonomy, verification, operator burden, persistent state, model adaptation, and operator learning.

If the FIRST approach remains informal, it can drift after seeing competitor results and become impossible to evaluate fairly.

A neutral control is also required so the lab can detect when every methodology adds more process than value.

## Decision

Freeze **FIRST-mode v0** as a named experimental treatment before the first runtime benchmark.

The canonical specification is:

- [FIRST-mode v0](../approaches/FIRST_MODE_V0.md)

The top-level full-workflow comparison has four arms:

1. Neutral/plain agent control.
2. Pinned pstack workflow.
3. Pinned Matt Pocock workflow.
4. FIRST-mode v0.

Mechanism-isolation experiments remain primary for causal understanding. The four-arm comparison is a system-level comparison, not a substitute for mechanism tests.

## Fairness rule

Once a controlled treatment round begins, FIRST-mode v0 cannot be edited in response to observed results.

Any substantive change produces a new version and a new comparison round.

The same applies to task prompts, oracle intent, scoring rules, and starting commits.

## Why FIRST-mode is separate from the operator profile

FIRST-mode is an **agent operating contract**.

Operator preferences are evaluation context and may influence the research question, but the treatment itself must still satisfy correctness, safety, verification, and maintainability.

A result does not win merely because it feels more pleasant to the operator.

## Consequences

The lab can now compare:

```text
Neutral
vs pstack
vs Matt Pocock
vs FIRST-mode v0
```

while still decomposing results by mechanism.

A FIRST-mode failure is a valid research result and should not be hidden.

FIRST-mode remains experimental until it passes the normal graduation path:

`research -> experiment -> evidence -> proposal -> FIRST architecture review -> production implementation`
