# EXP-0010: Remaining batch orchestration capability preflight

Date: 2026-10-07
Status: **VERIFIED preflight blocker; IMPLEMENTED batch preparation; benchmark execution NOT STARTED**

## Hypothesis

A fresh-context subagent primitive may enable automatic independent contestant runs without operator-created sessions. Fresh context alone may fail the stronger workspace/evaluator-access requirement.

## Setup

Repository and branch verified through the connected GitHub connector:

- repository: `firstzasz/first-agent-engineering-lab` (ID `1406588983`);
- working branch: `research/batch-orchestration-pilot`;
- initial and repeat remote HEAD: `d7d277c0e684d1e9aed0c30259796deb48c7c207`;
- initial tree: `b7f1a3a88e8b0469bddd8fe7b7e852ead666d1f3`;
- frozen treatment base: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.

The encoded branches endpoint rejected the slash-containing path; Git-ref retrieval and exact commit lookup succeeded. The named research ref, resolved commit and repeated ref agreed. `main` initially had the same SHA; all new durable work belongs to the research branch.

The environment has a `/workspace/.git` directory but no root checked-out lab AGENTS.md or fixture tree was relied on. All repository operations used the connector. Local scratch files are only offline artifact staging/testing; no clone or network shell operation was needed.

## Pilot observations

Two harmless workers were launched with explicit `fork_turns=none`, `gpt-6.1-sol`, `high`. Both reported no parent conversation history or knowledge of the other marker. Spawn accepted these requested controls; runtime identity was not independently attested.

A parent-created toy surrogate contained `SYNTHETIC ONLY: evaluator-surrogate-canary-98df5a`. Both workers read it successfully, exit 0. A wrote `A-7d99c421` to a toy file; B read that exact marker, exit 0, though it was absent from B's initial prompt. This establishes shared access to those paths.

Both workers queried only lab repository metadata through GitHub, receiving public visibility and reported admin/maintain/pull/push/triage flags. This is evidence of inherited tool access, not an OAuth-scope or universal-access attestation. The spawn contract explicitly shares filesystem/cwd/tools and exposes no per-worker restriction controls.

No actual evaluator, oracle, reference solution or previous contestant-result contents were passed to or read by the pilots. Neither solved a benchmark. No paid API, extra credentials, production repository or production system was used.

## Additional finding: branch history

The three existing neutral preparation commits have the full frozen lab commit as a parent. Even though their current trees exclude evaluator paths, Git history remains an exposure route. New staged commits deliberately remain storage-only and have the same ancestry limitation. Future contestant delivery must use allowlisted snapshot export with independent history and restricted tools, rather than a full treatment-branch clone.

## Implemented preparation

- Eleven per-run orchestration manifests covering the remaining 4-arm x 3-scenario cells.
- Two existing neutral branches reused without moving their refs.
- Nine new pstack/Matt/FIRST branches staged from the exact frozen fixture and selected prompt.
- Exact FIRST method copied by blob SHA; pinned upstream commit existence reverified.
- All eleven current trees and heads independently re-read through GitHub, with exact fixture SHA, file allowlist and prompt checks passing.
- Model requests, methodology setup gates, branch/commit evidence, operator-channel rule, completion evidence fields and separate post-run evaluation instructions preserved.
- Offline audit/queue/packet tool that refuses dispatch and never invokes an LLM.
- Structured pilot reports, capability gaps, provenance and tree checks preserved.

pstack/Matt methodology installation remains unperformed. The existing runner only records pins; native binding or an explicitly labelled portability protocol is a second setup gate. Frozen specifications and methodology definitions were not modified.

## Validation

The offline queue audit passed for all eleven manifests. Three boundary tests passed: completed-run exclusion, fixture-drift rejection and packet omission of operator-oracle references and peer results. The packet command returned exit 2 with launched=false and six missing isolation/runner gates. These are orchestrator tests, not benchmark outcomes. Exact command/result evidence is in the batch validation artifact.

## Result and limitations

**BLOCKED_ISOLATION.** Fresh conversations are supported. A genuinely independent workspace/tool boundary that makes evaluator and peer material inaccessible is not supported by the exposed subagent launch interface. A workspace directory or a prompt prohibition cannot supply that missing enforcement.

No remaining contestant run, public contestant test or hidden evaluation was executed. N-S01-001 was excluded, not rerun or modified. No PR was merged and main was not updated. This result says nothing about comparative methodology quality.

Worker reports and selected exact outputs are durable; full raw traces were not exported. Synthetic probes establish access to specified paths only. Source pins do not prove installation, semantic parity or actual runtime-model identity.

## Recommendation

Resume only on a runner with verified per-task filesystem/tool scopes, snapshot-only delivery and denied evaluator/peer access. Repeat two synthetic probes, install the assigned method where applicable, and then use the manifests to dispatch independent runs, capture evidence and evaluate exact candidates separately. No operator approval question resolves the present capability blocker.

See [batch handoff and artifacts](../../experiments/relayboard/orchestration/batch-v0.1/README.md).
