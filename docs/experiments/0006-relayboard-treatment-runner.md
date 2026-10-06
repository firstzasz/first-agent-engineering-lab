# EXP-0006: RelayBoard treatment-runner protocol

Status: VERIFIED

Date: 2026-10-06

## Hypothesis

A small runner can create comparable evaluator-blind workspaces from the frozen start SHA and preserve enough metadata to evaluate treatment outputs reproducibly.

## Setup

Frozen start commit:

`3a3315c3647474a03842d9405bb9a23aa41681b6`

Pilot scenarios:

- S01-v0
- S02-v0.1
- S04-v0

## Implementation

Added:

- `experiments/relayboard/runner/prepare_workspace.py`
- `experiments/relayboard/runner/evaluate_workspace.py`
- `experiments/relayboard/runner/selftest.py`
- `experiments/relayboard/runner/RUN_RECORD_TEMPLATE.json`
- runner documentation

The preparation step:

- exports only `fixtures/relayboard/` from the exact frozen commit;
- extracts the exact frozen task prompt from that commit;
- excludes evaluator material;
- records scenario, treatment, host, model, and pinned upstream metadata;
- initializes a clean standalone git repository for diff capture.

FIRST-mode v0 is copied into its treatment workspace as a frozen `METHOD.md`.

Pinned upstream treatments record provenance but do not copy upstream source; host-native setup remains a separate adapter concern.

The evaluator step:

- runs public tests against the modified workspace;
- loads the lab-side evaluator outside the treatment workspace;
- captures oracle failures;
- captures git diff/status/commit evidence.

## Expected behavior

CI should prove that:

1. S01/S02/S04 neutral workspaces can be prepared from the exact frozen SHA;
2. no evaluator directory leaks into them;
3. public baseline tests pass inside each prepared workspace;
4. the prepared workspaces are clean git repositories;
5. FIRST-mode v0 is pinned into its treatment workspace.

## Evidence

- PR #8
- merge commit: `42138f0907b2ff15e6a10c8ea41c4737a0351488`
- GitHub Actions run: `37470330930`
- `public-tests`: PASS
- `evaluator-red-capability`: PASS
- `treatment-runner`: PASS
- runner self-test output confirmed clean evaluator-blind workspaces from frozen base SHA and passing public tests

## Limitations

- The runner does not execute an LLM by itself.
- Operator interaction logs still depend on the host/orchestrator recording them.
- Native pstack and Matt setup remain host-specific.
- A public agent with unrestricted internet could deliberately fetch evaluator files; that remains a contamination rule rather than a secrecy guarantee.

## Result

SUPPORTED.

The runner can reproducibly prepare clean evaluator-blind workspaces from the frozen fixture SHA and preserve a stable evaluation boundary.

## Recommendation

Execute the neutral-control pilot next, one fresh evaluator-blind context per scenario, and preserve every run even if it fails.
