# Remaining RelayBoard batch v0.1

Status: **IMPLEMENTED preparation; VERIFIED current-tree provenance; BLOCKED execution**

This is the orchestrator control plane. Do not provide this directory, research index, experiment record or its evidence to a contestant. No remaining benchmark has run.

The eleven manifests in `runs/` exclude completed, independently verified `N-S01-001`. Its record, treatment branch and PR remain untouched. Source of truth: `research/batch-orchestration-pilot` in `firstzasz/first-agent-engineering-lab`.

## Capability finding

Two actual pilot workers were launched with `fork_turns=none`, `model=gpt-6.1-sol`, `reasoning_effort=high`. Each reported no inherited parent conversation or other worker marker. This supports separate task contexts, not complete isolation.

Both could read a parent-created synthetic evaluator surrogate. Worker B then read A's marker through the shared filesystem despite not receiving it in its initial prompt. Both had the same GitHub tools and successfully queried public lab metadata. Reported repository permission flags were broad; they are not an OAuth-scope attestation. Spawn has no per-worker filesystem, connector, branch or network restriction parameters.

No actual evaluator/oracle/reference-solution or contestant-results content was read by either pilot. Synthetic evidence is preserved under `evidence/pilot-a.json` and `evidence/pilot-b.json`. Full raw execution traces and independent runtime-model attestations were not exported; do not infer them.

The current environment **cannot satisfy the user's required inaccessible evaluator and peer-material boundary**. No contestant was launched. The available interface supports fresh contexts but does not expose a suitable isolated runner adapter. This is a capability blocker, not an operator approval gate.

## Frozen preparation

All fixture blobs and extracted task prompts come from Pilot Start State v0.1:

`2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`

FIRST-mode branches contain the exact frozen method blob `22ef0c77d90c3410785dd593f2b5c161edaed531`. pstack and Matt source pins were reverified via the connector. Their packages have **not** been installed:

- pstack: `cursor/plugins`, `pstack/`, `df581122cde17e6e27686b5a448bde23e4ad4318`;
- Matt: `mattpocock/skills`, `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`.

The lab runner records these pins but does not install or adapt upstream methodologies. Native installation and host behavior must be verified before those six runs. Source notes and generated summaries are not substitutes. Preserve upstream source/license. If a non-native host changes behavior, establish and label a portability protocol rather than silently treating it as a matched native comparison.

Two existing neutral branches were reused without changes. Nine other current-tree workspaces were created through GitHub Git-data operations, not by a local clone. All eleven branch heads, exact file allowlists, fixture blob SHAs, task prompts and FIRST method blob were re-read and checked through GitHub. Evidence: `evidence/workspace-verification.json`.

| Run | Scenario | Staged branch | Prepared SHA |
| --- | --- | --- | --- |
| N-S02-001 | S02-v0.1 | `treatment/neutral/N-S02-001` | `2fcdf1702b93bb2beb79add5dc57d8b82e3bda22` |
| N-S04-001 | S04-v0 | `treatment/neutral/N-S04-001` | `58e55eebad654c357934b93b639e6ba91f6d235d` |
| P-S01-001 | S01-v0 | `treatment/pstack/P-S01-001` | `32a15dd6209996fab8f4e6e25f1e3e87bfae77d2` |
| P-S02-001 | S02-v0.1 | `treatment/pstack/P-S02-001` | `7b6ef64e88895ac6364ad2c978a93534fd80fbd6` |
| P-S04-001 | S04-v0 | `treatment/pstack/P-S04-001` | `690561f1b65b149e7260351139e01f341251a289` |
| M-S01-001 | S01-v0 | `treatment/matt/M-S01-001` | `53a1ab55cd6d120ae37995655b1112992b0849fa` |
| M-S02-001 | S02-v0.1 | `treatment/matt/M-S02-001` | `3519a95b24be9aea82fc682b5ad130c45dd31be5` |
| M-S04-001 | S04-v0 | `treatment/matt/M-S04-001` | `73ba44a607c235006dc6719b831fbcb00967c699` |
| F-S01-001 | S01-v0 | `treatment/first-mode/F-S01-001` | `ce705042fa918d2127f9c36f3860f60dc97dd92a` |
| F-S02-001 | S02-v0.1 | `treatment/first-mode/F-S02-001` | `ddfdae5562e3886e678c0f6b551ddad5e696aa81` |
| F-S04-001 | S04-v0 | `treatment/first-mode/F-S04-001` | `3b7de30cce433a1ae65dfc32cf157cc14dd21469` |

**Git history is not sanitized.** Existing neutral preparation commits and the nine new preparation commits have the full frozen lab commit as a parent. A clean current tree is insufficient: a contestant with lab history can recover evaluator content. Deliver only the allowlisted current-tree snapshot to a fresh standalone workspace with independent history and no lab remote. These staged branches are storage artifacts, not proof of access isolation.

## Offline queue tool

Only Python standard library is required. No network, credentials, paid API or LLM launch occurs:

```bash
python experiments/relayboard/orchestration/batch-v0.1/orchestrate.py audit
python experiments/relayboard/orchestration/batch-v0.1/orchestrate.py queue
python experiments/relayboard/orchestration/batch-v0.1/orchestrate.py packet --run-id N-S02-001
```

Audit returns zero on a consistent plan. Packet outputs a deliberately allowlisted **planned** contestant envelope and exits **2**, with `launched=false` and missing capability gates. It omits evaluator source references, answer sheets, results and peer run identifiers. There is no launch implementation to enable by flipping a JSON flag.

Manifests preserve exact branch/start SHA, model request, methodology source/pin, expected files, isolated operator channel, public-test command, post-completion evaluation instruction, evidence fields and a NOT_STARTED record. Null measurements mean unknown or unexecuted; they are never fabricated as zero.

## Resume without recreating the experiment

1. Supply a runner that starts genuinely fresh tasks and enforces separate per-run filesystem/tool/network scopes. Contestants must have no lab GitHub connector, lab filesystem/history, peer workspaces/results, or evaluator access. Keep connector operations in the orchestrator; the contestant edits only its snapshot.
2. Repeat two synthetic workers and demonstrate: independent task context, denied parent evaluator-surrogate access, denied cross-worker access, and denied evaluator/peer retrieval through every available tool. Preserve observed denial outputs and the scope configuration. Do not test by exposing real oracles.
3. Re-read each prepared branch ref, verify its exact SHA and allowlisted blobs, and export only that immutable snapshot. Reject moved refs; never overwrite or force-reset someone else's work. Initialize independent workspace history. Record actual host, model/reasoning controls and observed runtime evidence separately from requested settings.
4. Install and verify only the assigned frozen methodology. Neutral uses ordinary host defaults. FIRST reads exact METHOD.md. pstack/Matt use only their pinned installed packages; record invoked skills and host limitations. Methodology subagents, where needed, must inherit the same restrictions and stay inside that run.
5. Dispatch eligible runs in the manifest order using independent contexts; the default queue is serial to avoid unnecessary usage. S02 questions go to a separate answer-only operator process using the frozen v0.1 sheet. Answer only valid asked product/preference questions, never volunteer additional requirements; persist each question, answer, timestamp and classification.
6. Capture available execution trace, timestamps, checkpoints, questions, diff, commit history and public test output. Unknown process metrics stay unknown. Stop on usage limits and durably record the unfinished attempt. Preserve contamination evidence; do not erase or quietly rerun a contaminated run.
7. Terminate the contestant, freeze and verify candidate commit/tree SHA, then evaluate that exact snapshot in a separate evaluator context using the pinned lab harness. Keep evaluator material and results away from live contestants. Do not feed hidden failures back for a same-run retry.
8. Persist run/evaluation records and available evidence to this research branch through the connector. Candidate PRs target their own treatment branches, never main. No contestant PR may be merged into main.

No real security/product/cost/irreversible choice is currently pending. Resumption requires a different capability, not confirmation.
