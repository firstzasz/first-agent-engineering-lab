# RelayBoard Scoring v0

Status: FROZEN FOR PILOT

Date frozen: 2026-10-06

## Scoring philosophy

Do not collapse the pilot into one universal score.

Each run produces a profile.

Correctness and safety are hard constraints. Operator fit and process cost matter, but they do not compensate for an incorrect result.

## Common dimensions

### Correctness

Record:

- public acceptance: PASS / FAIL;
- evaluator acceptance: PASS / FAIL;
- hidden regression cases passed / total.

### Verification strength

Use the strongest level actually evidenced:

- **V0 SELF_REPORT**: agent says it works with no inspectable evidence.
- **V1 STATIC**: lint/type/compile/static checks only.
- **V2 TESTED**: executable tests exercise required behavior.
- **V3 MATCHING_SURFACE**: the real or equivalent runtime/user surface is verified.
- **V4 INDEPENDENT**: V3 plus independent evaluator/reviewer evidence.

Do not award a level because the methodology requires it. Award only what the run produced.

### Operator interaction

Classify every question/checkpoint:

- FACT_LOOKUP;
- REVERSIBLE_ENGINEERING_CHOICE;
- PRODUCT_OR_PREFERENCE_DECISION;
- IRREVERSIBLE_OR_SECURITY_GATE;
- TRUE_BLOCKER;
- LEGIBLE_CHECKPOINT, which does not request a response.

Record counts separately.

### Silent assumptions

Count decisions that materially affect required behavior but were neither supported by evidence nor legitimately delegated by the prompt/treatment.

### Process overhead

Record counts where observable:

- planning/spec artifacts;
- tickets/issues;
- subagents;
- checkpoints;
- tool calls;
- commits;
- files changed;
- lines changed;
- elapsed time;
- tokens, if the host exposes them.

Do not convert these directly to a penalty without scenario context.

### Rework

Record:

- reverted approaches;
- duplicate work;
- substantial rewrites;
- repeated completed work after handoff.

### Persistent state

Record whether a fresh reviewer could reconstruct:

- goal;
- decisions;
- done vs pending;
- evidence;
- next step.

Use PASS / PARTIAL / FAIL with notes.

### Learning value

Blind reviewer rubric, 0-2 each:

- rationale identifies the real decision rather than narrating mechanics;
- evidence that changed the direction is visible;
- rejected alternatives/hypotheses are recorded when materially relevant;
- explanation is concise enough to learn from.

Maximum 8. Use only for runs where legibility is part of the treatment. Do not treat absence as a correctness failure in opaque controls.

## Scenario-specific metrics

### S01 Tiny Change

Primary outcome:

- acceptance PASS;
- unrelated behavior unchanged.

Key comparison metrics:

- tool/action count;
- artifacts created;
- operator interruptions;
- diff size;
- verification level.

S01 is specifically designed to expose over-process.

### S02 Ambiguous Requirement

Primary outcome:

- all frozen product semantics implemented correctly.

Requirement-discovery profile:

- product decisions correctly surfaced / 4;
- product decisions silently assumed / 4;
- FACT questions unnecessarily escalated;
- reversible engineering choices unnecessarily escalated;
- contradictions introduced;
- durable decisions captured.

A treatment that guesses the oracle correctly without asking still receives a silent-assumption count.

### S04 Hard Bug

Primary outcome:

- duplicate alert defect eliminated;
- legitimate alerts for distinct Runs preserved;
- retry semantics preserved.

Debugging profile:

- valid red-capable feedback loop before fix: yes/no;
- steps to first valid red signal;
- root cause correctly identified: yes/no;
- speculative fixes before root cause;
- wrong files modified before root cause;
- regression test at correct seam: yes/no;
- original scenario reverified after fix: yes/no;
- evaluator regression cases passed / total;
- temporary instrumentation cleaned up: yes/no.

## Comparison rule

Report each treatment as a profile.

Example:

```text
Correctness: PASS
Verification: V3
Operator questions: FACT 0 / ENGINEERING 0 / PRODUCT 4
Silent assumptions: 0
Process overhead: 2 artifacts, 18 tool calls
Learning value: 7/8
```

A later decision may introduce weights, but weights must be declared before looking at the treatment results they will score.
