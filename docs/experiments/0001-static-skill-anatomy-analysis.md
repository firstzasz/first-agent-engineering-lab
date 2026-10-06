# EXP-0001: Static skill-anatomy extraction

Status: VERIFIED FOR STATIC SOURCE ANALYSIS

Date: 2026-10-06

Upstream snapshots:

- Lauren Tan / pstack: `df581122cde17e6e27686b5a448bde23e4ad4318`
- Matt Pocock / skills: `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`

## Hypothesis

Representative workflows from both upstreams can be normalized into the lab's common anatomy:

`Trigger -> Context -> Procedure -> Tools -> State -> Verification -> Output Contract`

If true, later experiments can compare mechanisms rather than repository brands.

## Setup

Read-only inspection of pinned upstream files. No upstream source was copied or modified. No production system, private data, credentials, or FIRST production repository was used.

Representative pstack sources included `poteto-mode`, bug-fix, `architect`, `arena`, `swarm`, `interrogate`, `autonomous-run`, `session-pickup`, `show-me-your-work`, and `how`.

Representative Matt Pocock sources included `grilling`, `domain-modeling`, `to-spec`, `to-tickets`, `codebase-design`, `diagnosing-bugs`, `implement-spec`, `code-review`, `handoff`, and `wayfinder`.

## Implementation

Created:

- `docs/comparisons/skill-anatomy-matrix-v0.md`
- `docs/SKILL_ANATOMY_TEMPLATE.md`

The matrix normalizes eight research dimensions and explicitly separates observed behavior from runtime hypotheses.

## Expected behavior

The static analysis should expose comparable mechanisms and identify concrete mechanism-level experiments without claiming a runtime winner.

## Observed behavior

The anatomy was applicable to both upstreams.

The strongest architectural contrast visible in source is:

- pstack centralizes task routing, autonomy rules, and multiple orchestration shapes around a mode/playbook system;
- Matt Pocock's repository emphasizes composable skills, durable domain/spec/ticket artifacts, and dependency-aware execution.

The analysis also exposed several plausible complementary mechanisms, especially around debugging, human interruption policy, persistent state, and graph-aware orchestration.

## Evidence

- `docs/comparisons/skill-anatomy-matrix-v0.md`
- `docs/SKILL_ANATOMY_TEMPLATE.md`
- pinned upstream SHAs in `docs/sources/registry.yaml`
- PR #2
- merge commit: `d22d6a381907907c202dfbf5a2af0998d851ddf3`

## Limitations

- Static source inspection cannot establish runtime quality.
- Only representative workflows were inspected, not every file in either upstream.
- Host behavior such as Cursor subagents, cloud execution, or plugin invocation was not executed.
- No model, token, latency, or operator-effort measurements were collected.
- Complementarity is a hypothesis until controlled experiments reproduce it.

## Result

SUPPORTED for the narrow hypothesis.

Both approaches can be decomposed into the same anatomy, allowing mechanism-level comparisons to be designed.

This does **not** support any claim that one approach or hybrid is better.

## Recommendation

Use the matrix to design mechanism-first synthetic scenarios. Prioritize question routing, debugging feedback loops, persistent task graphs, autonomous exit predicates, and verification because they are both important to FIRST-style work and meaningfully different across the inspected sources.
