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

## Phase 1: Comparative experiments

Status: **PLANNED**

Primary question:

> Which techniques from pstack and Matt Pocock's skills improve agent engineering outcomes under controlled synthetic tasks, and which benefits depend on a specific host or runtime?

Comparison dimensions:

1. requirement discovery
2. architecture/specification
3. task decomposition
4. execution
5. debugging
6. verification
7. session continuity
8. autonomy
9. multi-agent orchestration
10. portability

The experiment plan and metrics are in [docs/comparisons/phase-1-plan.md](./docs/comparisons/phase-1-plan.md).

## Next work

1. Design one small synthetic application and ambiguity-rich change request as the common benchmark fixture.
2. Define scoring rubrics and machine-checkable acceptance tests before running either approach.
3. Run a neutral baseline without pstack or Matt Pocock skills.
4. Run pstack and Matt Pocock treatments separately without modifying their source.
5. Compare evidence, not agent self-reports.
6. Document any promising hybrid pattern as a proposal, not as a production decision.
