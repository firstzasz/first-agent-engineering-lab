# Research Phase 1: pstack vs Matt Pocock Skills

Status: PLANNED

## Research question

Which techniques from pstack and Matt Pocock's skills improve engineering-agent outcomes on the same synthetic tasks, and which effects depend on vendor/runtime behavior?

The objective is not to crown a universal winner. The objective is to isolate portable patterns and their tradeoffs.

## Experimental sequence

1. **EXP-010 Neutral baseline:** solve the fixture without either upstream approach.
2. **EXP-011 pstack treatment:** run the same task using the pinned pstack workflow without modifying its source.
3. **EXP-012 Matt Pocock treatment:** run the same task using the pinned skills workflow without modifying its source.
4. **EXP-013 Fresh-session pickup:** interrupt each treatment at a controlled boundary and measure recovery by a fresh agent.
5. **EXP-014 Debugging challenge:** introduce a deterministic defect with a hidden but machine-checkable root cause.
6. **EXP-015 Multi-agent graph:** use a task with parallelizable and blocked slices, then measure duplication, conflicts, and wall-clock progress.
7. **EXP-016 Portability probe:** run selected principles/workflows on at least one non-native host and record adaptation cost and semantic loss.
8. **EXP-017 Hybrid candidate:** only if earlier evidence identifies complementary strengths, test a minimal hybrid instead of combining everything.

## Common fixture requirements

The fixture must be synthetic, small enough to inspect, and rich enough to exercise ambiguity, architecture, implementation, debugging, tests, handoff, and parallel work.

Before treatments run, freeze:

- initial repository commit
- task prompt
- acceptance tests
- hidden defect or oracle where used
- scoring rubric
- time/token/tool budgets where measurable

Do not tune the fixture after seeing one treatment's result unless a new version is created for all treatments.

## Comparison dimensions and measures

| Dimension | Evidence to collect |
| --- | --- |
| Requirement discovery | unresolved ambiguities, empirically answerable questions unnecessarily escalated to the user, requirement misses, durable decisions captured |
| Architecture/specification | explicit data/module decisions, contradictions, scope control, spec-to-implementation traceability |
| Task decomposition | slice completeness, dependency correctness, ready-frontier utilization, stale or redundant tickets |
| Execution | acceptance-test completion, rework count, unnecessary diff size, blocked time |
| Debugging | reproduction before fix, feedback-loop quality, hypothesis trace, time/steps to root cause, regression evidence |
| Verification | automated checks, false-green rate, independent review findings, claims backed by evidence |
| Session continuity | fresh-agent reconstruction accuracy, missing decisions, time/steps to resume, duplicated work |
| Autonomy | operator interruptions, unsafe assumptions, unnecessary questions, recoverability, audit trail |
| Multi-agent orchestration | useful parallelism, duplicate work, merge conflicts, coverage gaps, coordination overhead |
| Portability | host-specific primitives, required adaptation, behavior lost or changed, setup complexity |

## Scoring rules

Use a mix of machine checks and blinded human review where possible.

Prefer binary or countable evidence over vibes. Examples:

- acceptance tests: pass/fail
- hidden defect: found/not found
- unnecessary user questions: count
- verified claims: supported/unsupported count
- duplicated edits: overlapping diff or duplicated task count
- resume completeness: checklist score against pre-recorded state
- portability adaptation: changed files/lines plus qualitative semantic-loss notes

Any subjective rubric must be written before reviewing treatment labels.

## Controls

- Same synthetic repository and task inputs.
- Same starting commit.
- Same secrets policy: none.
- No private FIRST data or production access.
- Pin upstream source snapshots.
- Preserve raw evidence.
- Do not let one treatment edit the other treatment's instructions.
- Separate host limitations from methodology limitations in the final comparison.

## Exit criteria

Phase 1 completes only when each claimed finding points to reproducible evidence and its limitations are recorded.

Promising patterns may then move to `docs/proposals/`. Nothing moves directly to FIRST production.
