# Research Index

Last updated: 2026-10-06

## Status legend

- **IMPLEMENTED**: artifact or structure exists in this repository.
- **VERIFIED**: state has been independently checked against GitHub or executable evidence.
- **PLANNED**: approved research direction, not yet executed.

## Phase 0: Lab bootstrap

Status: **IMPLEMENTED and VERIFIED**

Scope:

- public research repository structure
- operating contract and public-repo safety boundary
- experiment template
- upstream source registry
- read-only architecture inspection for pstack and Matt Pocock skills
- Research Phase 1 comparison plan

Important constraint: no pstack or Matt Pocock skill source was copied into this repository during Phase 0.

Verification evidence:

- Bootstrap PR #1 was merged to `main` as `41be211bd46799ff1bd0f3a37b17f9c2cfe8ce52`.
- The merged `main` tree was re-read from GitHub and the required root directories/files were present.
- The official upstream snapshots were re-queried after merge and still matched the registry.
- PR #1 had no configured commit-status checks. Phase 0 verification is therefore repository-state/provenance verification, not runtime behavior verification.
- Detailed record: [docs/experiments/0000-bootstrap.md](./docs/experiments/0000-bootstrap.md).

## Upstream snapshots inspected

| Source | Official upstream | Snapshot |
| --- | --- | --- |
| Lauren Tan / pstack | `cursor/plugins` under `pstack/` | `df581122cde17e6e27686b5a448bde23e4ad4318` |
| Matt Pocock / skills | `mattpocock/skills` | `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d` |

See [docs/sources/registry.yaml](./docs/sources/registry.yaml) for provenance and licensing.

## Research methodology decisions

**ADR-0003: capability-adaptive, legible autonomy.**  
Agent autonomy should vary by measured model/task capability and risk, but verification remains external. Long or important runs should expose concise engineering checkpoints so the operator can audit and learn without becoming a blocking approval gate.

See:

- [ADR-0003](./docs/adrs/0003-capability-adaptive-legible-autonomy.md)
- [Legible Autonomy Research Framework](./docs/LEGIBLE_AUTONOMY.md)



**ADR-0001: contextual fit over a universal methodology winner.**  
Compare approaches by task class, host constraints, evidence strength, process overhead, and operator fit. Evidence-supported hybrids are allowed.

**ADR-0002: skill engineering as portable procedural knowledge.**  
Study the durable anatomy and behavior of reusable procedures rather than treating today's `SKILL.md` format as the research target.

See:

- [ADR-0001](./docs/adrs/0001-contextual-fit-over-universal-winner.md)
- [ADR-0002](./docs/adrs/0002-skill-engineering-as-portable-procedural-knowledge.md)
- [Skill Engineering Research Thesis](./docs/SKILL_ENGINEERING.md)

## Long-term skill-engineering questions

The lab aims to build evidence for deciding:

1. what belongs in knowledge/context;
2. what belongs in memory or explicit persistent state;
3. what should be a reusable skill or procedure;
4. what should be an executable tool;
5. what should be composed into a larger workflow;
6. what should be enforced by code, tests, schemas, CI, or policy rather than prose;
7. how the answer changes by task type, operator style, and agent host.

The common analysis frame is:

`Trigger -> Context -> Procedure -> Tools -> State -> Verification -> Output Contract`

## Phase 1: Comparative experiments

Status: **PLANNED**

### Phase 1B: Mechanism benchmark design

Status: **IMPLEMENTED and VERIFIED**

The benchmark design is documented in [Mechanism Benchmark Design v0](./docs/comparisons/mechanism-benchmark-design-v0.md), with [EXP-0002](./docs/experiments/0002-mechanism-benchmark-design.md) recording the design result.

Verification evidence:

- PR #3 merged to `main` as `b28a076bf4615303a85910c2941441e7a2f833c4`.
- The merged benchmark design and EXP-0002 record were re-read from `main` after merge.
- PR #3 had no configured commit-status checks, so this verifies repository state and design persistence, not runtime treatment behavior.

The shared synthetic system is provisionally named **RelayBoard**. Eight scenarios are defined, but implementation is intentionally staged. The first fixture slice will support S01 tiny reversible change, S02 ambiguous requirement, and S04 deterministic hard bug before broader orchestration scenarios are built.

### Phase 1A: Static skill anatomy

Status: **IMPLEMENTED and VERIFIED**

The first mechanism-level analysis is complete:

- [Skill Anatomy Matrix v0](./docs/comparisons/skill-anatomy-matrix-v0.md)
- [Reusable Skill Anatomy Template](./docs/SKILL_ANATOMY_TEMPLATE.md)
- [EXP-0001 static analysis record](./docs/experiments/0001-static-skill-anatomy-analysis.md)

Verification evidence:

- PR #2 merged to `main` as `d22d6a381907907c202dfbf5a2af0998d851ddf3`.
- The merged matrix, template, and EXP-0001 record were re-read from `main` after merge.
- The official upstream latest-commit queries were repeated before merge and still matched the pinned registry SHAs.
- PR #2 had no configured commit-status checks, so this verifies repository state and source provenance, not runtime workflow quality.

The analysis normalizes representative upstream workflows into:

`Trigger -> Context -> Procedure -> Tools -> State -> Verification -> Output Contract`

It identifies mechanism-level hypotheses for requirement discovery, architecture, decomposition, debugging, verification, continuity, autonomy, orchestration, and portability. Runtime quality is not yet claimed.

Primary question:

> Which techniques improve agent engineering outcomes for different task classes, and which combination best fits FIRST workflows without unnecessary process overhead?

Scenario families include requirement discovery, architecture, feature work, debugging, verification, handoff, autonomous work, multi-agent execution, product iteration, and deliberately small changes.

Phase 1 will also extract skill anatomy from the tested approaches so a successful result can be attributed to reusable mechanisms rather than merely to a repository name.

The experiment plan and metrics are in [docs/comparisons/phase-1-plan.md](./docs/comparisons/phase-1-plan.md).

## Next work

1. Freeze the RelayBoard domain glossary and S01/S02/S04 prompts, including model-capability and legibility treatment metadata.
2. Define public acceptance tests, hidden-oracle intent, and scoring rubrics for S01/S02/S04 before treatment runs.
3. Implement only the minimal fixture needed for those three scenarios.
4. Pilot neutral baselines before pstack and Matt Pocock treatments.
5. Calibrate operator-interruption and process-overhead measurements.
6. Expand to architecture, verification-trap, pickup, autonomy, and multi-agent scenarios only after the harness proves useful.
7. Compare evidence by scenario and mechanism rather than declaring an overall winner.
8. Test a minimal hybrid only after individual strengths are demonstrated.
