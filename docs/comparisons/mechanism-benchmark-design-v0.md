# Mechanism Benchmark Design v0

Status: DESIGN COMPLETE, implementation not started

Date: 2026-10-06

Depends on:

- [Skill Anatomy Matrix v0](./skill-anatomy-matrix-v0.md)
- [ADR-0001: contextual fit over a universal methodology winner](../adrs/0001-contextual-fit-over-universal-winner.md)
- [ADR-0002: skill engineering as portable procedural knowledge](../adrs/0002-skill-engineering-as-portable-procedural-knowledge.md)

## Goal

Turn the static skill-anatomy hypotheses into controlled, mechanism-level experiments.

The benchmark must answer questions such as:

- Does facts-first question routing reduce operator interruption without increasing wrong assumptions?
- Does feedback-loop-first debugging improve root-cause accuracy?
- When does a persistent dependency graph pay for its ceremony?
- Does an explicit autonomous exit predicate improve completion and recovery?
- Does same-surface verification catch false greens that tests alone miss?

It must **not** answer only "pstack or Matt Pocock?"

## Shared synthetic system

Working name: **RelayBoard**.

RelayBoard is a small synthetic job-control application. It deliberately resembles ordinary engineering work without containing FIRST production logic or financial data.

Provisional domain:

- **Job**: a configured unit of scheduled work.
- **Run**: one execution attempt of a Job.
- **RetryPolicy**: rules controlling retry behavior.
- **AlertRule**: rules that emit a notification after a Run outcome.
- **Dashboard**: small read-only/operator UI for jobs and recent runs.

Provisional implementation shape:

- Python application;
- small HTTP API;
- SQLite persistence;
- minimal HTML/JS dashboard;
- deterministic test suite;
- fake clock and fake notification adapter;
- containerized execution where useful for artifact verification.

The final implementation choice remains reversible until fixture work begins. The benchmark design does not depend on FastAPI, Flask, or a particular UI framework.

## Why one shared system

Keeping the domain and codebase stable reduces noise while allowing different branches to exercise different mechanisms.

Each scenario gets:

- a frozen starting commit;
- one task prompt;
- public acceptance tests;
- hidden oracle checks where needed;
- a scoring rubric frozen before treatments run;
- a known expected state transition.

No treatment may change another treatment's instructions or oracle.

## Scenario suite

### S01: Tiny reversible change

**Purpose**

Measure process overhead and whether a methodology scales down gracefully.

**Task shape**

A one-file behavior or UI wording change with an obvious acceptance test and no architectural ambiguity.

**Mechanism under test**

- lightweight execution vs heavy workflow ceremony;
- automatic routing threshold;
- verification proportional to risk.

**Key measures**

- elapsed/tool steps to completion;
- number of generated artifacts;
- operator interruptions;
- diff size;
- acceptance result;
- unsupported "done" claims.

**Failure mode we want to detect**

A rigorous workflow that turns a five-minute change into unnecessary planning, tickets, or agent fan-out.

---

### S02: Ambiguous product requirement

**Purpose**

Measure question classification and requirement discovery.

**Task shape**

Add "pause a Job" with deliberately unresolved semantics:

- what happens to a Run already in progress?
- what happens to a scheduled Run whose start time occurs while paused?
- can a paused Job be manually run?
- is resume immediate or schedule-based?

Some questions are product decisions. Other facts can be learned from code.

**Mechanism under test**

- naive ask-user behavior;
- facts-first investigation;
- Matt-style decision frontier;
- pstack-style refusal to ask empirically answerable questions;
- durable glossary/decision capture.

**Key measures**

- unnecessary factual questions to operator;
- genuine product decisions correctly surfaced;
- silent assumptions;
- requirement misses;
- contradictory decisions;
- durable decisions recorded;
- implementation correctness after decisions.

**Primary hypothesis**

A hybrid facts-first + decision-frontier policy reduces interruption while preserving requirement quality.

---

### S03: Architecture under uncertainty

**Purpose**

Measure whether design-space exploration and durable domain/seam criteria improve architecture.

**Task shape**

Add per-Job retry behavior with:

- global default;
- per-Job override;
- bounded attempts;
- fake clock support for deterministic tests;
- no duplicated retry logic across API and worker paths.

**Mechanism under test**

- single-design implementation;
- design-twice / arena exploration;
- deep-module and seam vocabulary;
- domain modeling;
- durable spec.

**Key measures**

- number of public interfaces introduced;
- duplicated policy logic;
- test seam quality;
- invalid states representable;
- rework after implementation begins;
- reviewer-rated maintainability using a blinded rubric;
- process overhead.

**Primary hypothesis**

Design-twice helps when multiple plausible structures exist, but only if paired with a crisp selection rubric.

---

### S04: Deterministic hard bug

**Purpose**

Measure debugging discipline.

**Injected defect**

Under a specific retry path, a Run can emit the same alert twice because an operation that must be idempotent is performed at the wrong lifecycle point.

The visible symptom is duplicate notifications. The root cause is not in the notification adapter itself.

**Mechanism under test**

- code-reading-first debugging;
- feedback-loop-first debugging;
- pstack-style binary search and same-surface verification;
- Matt-style tight red-capable loop, minimisation, ranked falsifiable hypotheses, instrumentation.

**Key measures**

- time/steps to first valid red signal;
- time/steps to root cause;
- incorrect files changed before root cause;
- speculative fixes attempted;
- minimal repro quality;
- regression test quality;
- original-surface verification;
- recurrence under hidden tests.

**Primary hypothesis**

Feedback-loop-first plus same-surface closure beats either tests-only or intuition-led debugging.

---

### S05: Verification trap

**Purpose**

Measure false-green resistance.

**Task shape**

A code change makes unit/integration tests pass, but the built container or served UI still contains a stale artifact unless the correct build/runtime path is exercised.

**Mechanism under test**

- tests-only completion;
- real-artifact verification;
- same-surface verification;
- evidence capture.

**Key measures**

- whether the treatment declares done before checking the built artifact;
- hidden artifact-version check;
- runtime behavior;
- evidence quality;
- false-green rate.

**Primary hypothesis**

Explicit real-artifact verification catches a class of failures that ordinary test completion misses.

---

### S06: Session interruption and pickup

**Purpose**

Measure persistent state and restart cost.

**Task shape**

Interrupt a multi-step feature after a controlled milestone. A fresh agent receives only the repository/tracker state allowed by the treatment.

**Mechanism under test**

- prose-only handoff;
- decision trail + branch state reconstruction;
- persistent spec/tickets/ADRs;
- compact context pointers;
- independent verification of inherited claims.

**Key measures**

- time/steps to identify resume point;
- completed work unnecessarily repeated;
- lost decisions;
- wrong assumptions about landed work;
- number of questions required to resume;
- final acceptance result.

**Primary hypothesis**

Durable task state plus a compact pickup pointer outperforms transcript-style prose as the sole handoff mechanism.

---

### S07: Long autonomous run

**Purpose**

Measure autonomous completion without excessive operator involvement.

**Task shape**

A multi-step migration with deterministic intermediate failures and one related reversible issue discovered mid-run.

**Mechanism under test**

- open-ended "keep going";
- explicit exit predicate;
- reversible-work ownership;
- checkpoint evidence;
- HITL/AFK classification.

**Key measures**

- operator interruptions;
- premature stop count;
- exit predicate clarity;
- recovery from injected failure;
- unrelated scope creep;
- quality of checkpoints;
- final verified state.

**Primary hypothesis**

A checkable exit predicate plus clear pause boundaries improves autonomy without increasing unsafe assumptions.

---

### S08: Parallel dependency graph

**Purpose**

Measure orchestration quality rather than raw agent count.

**Task shape**

A feature with:

- two immediately parallelizable vertical slices;
- one ticket blocked on both;
- one architecture choice where competing full designs are useful;
- one final review gate.

**Mechanism under test**

- generic fan-out;
- persistent dependency graph and ready frontier;
- swarm for partitioned coverage;
- arena for alternatives;
- independent adversarial review.

**Key measures**

- useful parallel work ratio;
- duplicate work;
- blocked work started too early;
- merge conflicts;
- missing dependencies;
- wall-clock progress where measurable;
- coordination artifacts created;
- final acceptance result.

**Primary hypothesis**

Dependency state should choose what can run, while orchestration shape should choose how it runs.

## Model capability and legibility axis

Selected scenarios should be repeated across different model capability levels where practical.

The workflow is allowed to adapt to measured model/task capability, but the acceptance oracle must not change.

Record:

- model and host;
- calibration status on that task class;
- procedure/scaffolding enabled;
- independent review requirements;
- checkpoint frequency;
- operator-visible rationale artifacts;
- acceptance and false-green outcomes.

Do not use model self-confidence as the only calibration signal.

At least one treatment should test **legible autonomy**: the agent continues without approval after reversible decisions while emitting concise checkpoints containing evidence, decision, alternatives materially considered, verification result, remaining uncertainty, and next step.

This allows the benchmark to ask whether stronger models can safely use lighter scaffolding while retaining external verification and operator learning value.

## Cross-scenario metrics

Every scenario records:

| Metric | Meaning |
| --- | --- |
| Correctness | Public + hidden acceptance result |
| Verification strength | How strongly the final claim is backed by executable evidence |
| Operator interruption | Count and classification of questions/checkpoints |
| Wrong assumptions | Unverified decisions made where evidence or a required human decision existed |
| Rework | Work discarded or substantially redone |
| Process overhead | Setup, docs, tickets, agents, and coordination relative to task size |
| Persistent state quality | Whether a fresh agent can reconstruct decisions and progress |
| Recovery | Ability to continue after injected failure/interruption |
| Portability | Host-specific steps or semantic degradation |
| Diff discipline | Unnecessary changes beyond the justified scope |

## Operator-fit classification

Every operator interaction must be labeled as one of:

1. **FACT_LOOKUP**: agent could determine it from code, tools, runtime, or documentation.
2. **REVERSIBLE_ENGINEERING_CHOICE**: agent could safely choose under an autonomy grant and record the choice.
3. **PRODUCT_OR_PREFERENCE_DECISION**: requires human judgment or desired behavior.
4. **IRREVERSIBLE_OR_SECURITY_GATE**: requires explicit approval.
5. **TRUE_BLOCKER**: missing access/capability prevents safe progress.

This turns "annoying vs not annoying" into evidence.

## Treatment strategy

Do not begin with repository-vs-repository full-stack comparisons.

For each scenario:

1. run a neutral baseline;
2. test the smallest isolated mechanism likely to matter;
3. only then run the upstream-native workflow;
4. if two mechanisms look complementary, test the minimal hybrid;
5. keep treatment labels blinded during subjective review where practical.

Example for S04 debugging:

- A: neutral baseline;
- B: feedback-loop-first only;
- C: same-surface verification only;
- D: combined mechanism;
- E: pinned upstream-native pstack;
- F: pinned upstream-native Matt workflow.

This lets the lab identify **why** an outcome improved.

## FIRST-fit weighting

Do not choose final weights yet.

Before any composite score exists, estimate the real distribution of FIRST work categories from repository history or a synthetic proxy. Until then, report profiles by scenario.

A future composite score may weight:

- feature/change work;
- debugging;
- architecture;
- maintenance/small changes;
- long autonomous work;
- multi-session work;
- orchestration-heavy work.

The weights must be declared before scoring treatments.

## Fixture implementation gates

RelayBoard implementation begins only after these are frozen:

- domain glossary;
- scenario IDs and prompts;
- public acceptance tests;
- hidden oracle intent;
- metric definitions;
- treatment isolation rules.

The hidden tests themselves may be implemented later, but what they are intended to detect must be written first to avoid tuning the oracle after seeing results.

## Next implementation slice

Build only enough RelayBoard for **S01, S02, and S04** first.

Reason:

- S01 measures overhead;
- S02 measures operator interaction policy;
- S04 measures evidence-first debugging.

These three test mechanisms central to FIRST's preferred working style without requiring multi-agent infrastructure on day one.

S03, S05, S06, S07, and S08 should remain designed but unimplemented until the first three validate the harness.
