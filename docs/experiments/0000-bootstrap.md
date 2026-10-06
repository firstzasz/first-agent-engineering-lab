# EXP-0000: Bootstrap FIRST Agent Engineering Lab

Status: VERIFIED

Date: 2026-10-06

Upstream snapshots:
- Lauren Tan / pstack: `df581122cde17e6e27686b5a448bde23e4ad4318`
- Matt Pocock / skills: `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`

Fixture:
- None. Bootstrap is repository-structure and provenance work.

## Hypothesis

A public research repository can be bootstrapped with enough persistent structure, provenance, safety rules, and experiment discipline that future agent sessions do not need chat history as the source of truth.

## Setup

The repository initially contained only `README.md` and `LICENSE`.

Official upstream sources were inspected read-only through GitHub. The lab remained isolated from FIRST production systems and used no private data or credentials.

## Implementation

PR #1 added:

- `AGENTS.md`
- `RESEARCH_INDEX.md`
- source registry and two architecture inspection notes
- experiment documentation and template
- Phase 1 comparison plan
- proposal and ADR locations
- executable experiment and synthetic fixture locations
- explicit public-repository and production-isolation rules

No upstream pstack or Matt Pocock source was imported.

## Expected behavior

After merge, GitHub `main` should contain all required research paths, the registry should pin exact official snapshots and licenses, and Phase 1 should be resumable from repository documentation alone.

## Observed behavior

PR #1 merged successfully. The `main` tree was fetched after merge and contained:

- `README.md`
- `RESEARCH_INDEX.md`
- `docs/`
- `experiments/`
- `fixtures/`

Within `docs/`, the required sources, experiments, comparisons, proposals, and ADR paths were present.

The upstream latest-commit queries were repeated after the merge and still returned the same pinned SHAs stored in the registry.

## Evidence

- PR #1
- merge commit: `41be211bd46799ff1bd0f3a37b17f9c2cfe8ce52`
- bootstrap implementation commit before squash: `d07a23e456bad9675a7128122f3b0ca06bb87828`
- source registry: `docs/sources/registry.yaml`
- Phase 1 plan: `docs/comparisons/phase-1-plan.md`

## Limitations

- No agent workflow has been run yet, so there is no runtime evidence about pstack or Matt Pocock skills.
- No CI workflow is configured in the lab yet. PR #1 had no commit-status checks.
- Architecture notes are based on static inspection of selected upstream files and directory structure, not exhaustive semantic analysis.
- "Latest" means latest visible at the recorded check time. Future upstream commits will require a new registry update rather than silently moving the pinned snapshot.

## Result

SUPPORTED.

The persistent GitHub structure and provenance required for starting controlled research are present and were independently re-read after merge.

## Recommendation

Begin Phase 1 by creating the synthetic benchmark fixture and scoring oracle before installing or copying any upstream workflow. Run a neutral baseline first.
