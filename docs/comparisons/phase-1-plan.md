# Research Phase 1: Contextual Comparison of Agent Engineering Approaches

Status: PLANNED

## Research question

Which techniques from pstack and Matt Pocock's skills improve engineering-agent outcomes for different classes of synthetic tasks, which effects depend on vendor/runtime behavior, and which patterns fit FIRST's preferred operating style?

The objective is not to crown a universal winner. The objective is to isolate portable patterns, tradeoffs, task fit, and operator fit.

See [ADR-0001](../adrs/0001-contextual-fit-over-universal-winner.md).

## Mechanism extraction before benchmarking

Before judging outcomes, decompose representative workflows from each upstream into the same anatomy:

`Trigger -> Context -> Procedure -> Tools -> State -> Verification -> Output Contract`

For each workflow, also record:

- explicit vs implicit invocation;
- host-specific assumptions;
- operator interruption policy;
- persistence mechanism;
- failure and retry behavior;
- composability;
- process overhead;
- whether important behavior is merely instructed or actually enforced by executable checks.

This prevents the study from attributing a result to a repository name when the real cause is a reusable mechanism such as persistent task state, a dependency graph, adversarial review, or executable verification.

See [Skill Engineering Research Thesis](../SKILL_ENGINEERING.md) and [ADR-0002](../adrs/0002-skill-engineering-as-portable-procedural-knowledge.md).

## Benchmark design

Use one small synthetic system as the shared world where practical, but exercise it through multiple scenarios rather than treating one task as representative of all agent work.

Planned scenario families:

1. ambiguous requirement discovery;
2. architecture or greenfield design;
3. feature change inside an existing system;
4. hard deterministic debugging;
5. verification-heavy completion;
6. fresh-session pickup and handoff;
7. long autonomous execution;
8. parallel dependency-graph execution;
9. UI or product iteration where practical;
10. deliberately small change to measure process overhead.

Not every upstream approach must be expected to dominate every scenario. The point is to map where each technique helps, where it hurts, and what it costs.

## Experimental sequence

1. **EXP-010 Neutral baseline:** run representative scenarios without either upstream approach.
2. **EXP-011 pstack treatment:** run the same frozen scenarios using the pinned pstack workflow without modifying its source.
3. **EXP-012 Matt Pocock treatment:** run the same frozen scenarios using the pinned skills workflow without modifying its source.
4. **EXP-013 Fresh-session pickup:** interrupt each treatment at a controlled boundary and measure recovery by a fresh agent.
5. **EXP-014 Debugging challenge:** introduce a deterministic defect with a hidden but machine-checkable root cause.
6. **EXP-015 Multi-agent graph:** use a task with parallelizable and blocked slices, then measure duplication, conflicts, and wall-clock progress.
7. **EXP-016 Portability probe:** run selected principles/workflows on at least one non-native host and record adaptation cost and semantic loss.
8. **EXP-017 Hybrid candidate:** if earlier evidence identifies complementary strengths, test the smallest useful hybrid instead of combining everything.

## Common fixture requirements

The fixture must be synthetic, small enough to inspect, and rich enough to support multiple scenario branches.

Before treatments run, freeze for each scenario:

- starting commit;
- task prompt;
- acceptance tests;
- hidden defect or oracle where used;
- scoring rubric;
- time/token/tool budgets where measurable.

Do not tune a scenario after seeing one treatment's result unless a new version is created for all treatments.

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
| Operator fit | interruption burden, ceremony relative to task size, GitHub persistence, reviewability, recoverability, ease of adapting the workflow |
| Process overhead | setup time, generated artifacts, coordination steps, and work that does not directly improve the measured result |

## Interpretation rules

Do not collapse the whole study into a single score unless a specific decision later requires a weighted score.

Prefer a profile such as:

- strong for ambiguous discovery;
- weak for tiny fixes because of overhead;
- strong for autonomous recovery;
- host-dependent for orchestration.

If FIRST eventually needs a composite decision score, weights must reflect the real distribution and importance of FIRST task types and must be declared before scoring treatments.

## Scoring rules

Use a mix of machine checks and blinded human review where possible.

Prefer binary or countable evidence over vibes. Examples:

- acceptance tests: pass/fail;
- hidden defect: found/not found;
- unnecessary user questions: count;
- operator interruptions: count and reason;
- verified claims: supported/unsupported count;
- duplicated edits: overlapping diff or duplicated task count;
- resume completeness: checklist score against pre-recorded state;
- portability adaptation: changed files/lines plus qualitative semantic-loss notes;
- process overhead: setup and coordination actions relative to task size.

Any subjective rubric must be written before reviewing treatment labels.

## Controls

- Same synthetic repository and frozen scenario inputs.
- Same starting commit per scenario.
- Same secrets policy: none.
- No private FIRST data or production access.
- Pin upstream source snapshots.
- Preserve raw evidence.
- Do not let one treatment edit the other treatment's instructions.
- Separate host limitations from methodology limitations in the final comparison.
- Distinguish a method being "good in general" from being "fit for this task and operator."

## Exit criteria

Phase 1 completes only when each claimed finding points to reproducible evidence and its limitations are recorded.

Promising individual patterns or minimal hybrids may then move to `docs/proposals/`. Nothing moves directly to FIRST production.
