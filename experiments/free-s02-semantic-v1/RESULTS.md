# S02 Semantic Adjudication V1: no-inference replay results

**Date:** 2026-11-01 local (GitHub Actions executed 2026-10-31 18:35 UTC)  
**Status:** IMPLEMENTED and source-anchoring **VERIFIED**; semantic label validity **PROVISIONAL_UNBLINDED**, not independently or blindly validated.

## Why this exists

The frozen S02 G0–G3 scorer from [run #41222993755](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41222993755) was internally consistent, but an audit found false-positive, false-negative and cross-clause classifications. Its 4/4 score is therefore **not** reliable semantic coverage. The original V0 protocol, matcher, grading artifact and scores remain untouched.

This separate V1 scores the **four explicit product-policy contrasts**, not incidental topic words. Each credit must cite an exact question from the original workflow artifact; absent and partial questions receive no credit. See [RUBRIC.md](./RUBRIC.md), [ANNOTATIONS_PROVISIONAL.json](./ANNOTATIONS_PROVISIONAL.json) and [ADVERSARIAL_CASES.json](./ADVERSARIAL_CASES.json).

## Executable evidence

- Original V1 test run [#41230079816](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230079816) **FAILED** one overstrict test-fixture reason-length assertion. This failure is preserved, and test-contract correction was made without any inference.
- Corrected V1 workflow [#41230136405](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230136405) **SUCCESS**: **9/9** unit selftests passed; replay downloaded the unchanged original eight contestant transcripts plus frozen grader, verified every labeled question index+quote against the original source, and generated `semantic-v1-replay.json`.
- Total newly issued LLM inference requests in V1: **0**. No developer Secret injected in this workflow.
- Exact original source artifacts remain available under run #41222993755 until their 14-day retention period expires.

## Machine V0 score compared with provisional V1 review

| Mechanism | NVIDIA V0 auto | NVIDIA V1 provisional | OpenRouter V0 auto | OpenRouter V1 provisional |
|---|---:|---:|---:|---:|
| G0 Neutral | 4/4 | **2/4** | 3/4 | **2/4** |
| G1 Behavior Matrix | 4/4 | **2/4** | 3/4 | **3/4** |
| G2 Dependency Graph | 3/4 | **1/4** | 2/4 | **1/4** |
| G3 Coverage Loop | 3/4 | **2/4** | 3/4 | **1/4** |

The differences are not small: V0's substring-based matcher often gave `resume_behavior` for merely mentioning a resume endpoint, and counted scheduled blocking without asking whether a missed trigger is skipped or queued. Conversely, it missed manual-run plural forms and clear catch-up-vs-next-cycle questions.

**No leaderboard, model advantage or method winner is justified** by these provisional reviewed values: one reviewer knew the treatment labels, there is only one run per cell, and some policies are ambiguous. Deterministic replay verifies only provenance and arithmetic, not the correctness of human semantic judgment.

## Integrity and nuance

- V1 generated one review entry for each of the 4 frozen oracle contrasts in each of 8 run cells, with statuses `EXPLICIT`, `PARTIAL`, `ABSENT` and `NOT_ADJUDICATED`.
- Every `EXPLICIT` and `PARTIAL` points to a 1-based original question index plus exact source substring. Forged quotes and incorrect indices fail unit tests.
- `UNCLASSIFIED` V0 questions may be important **other** product requirements (e.g., dashboard visibility and disabled-vs-paused orthogonality), not useless questions.
- A whole-system comparison of pstack/Matt Pocock Skills/FIRST-mode plus Neutral has **not** yet been repeated with a fidelity-preserving harness; G0–G3 are smaller discovery mechanisms, not those three full methods.
- There has been no EXP-0017 C2 launch or change to FIRST production or `main`.

## Next research gate

1. Produce identity-blinded shuffled source-question packets from the frozen artifacts; use two independent human reviewers against [RUBRIC.md](./RUBRIC.md) and adjudicate disagreements. Existing labels are *hypotheses* for checking, not gold truth.
2. Check that a future scoring system rejects all 20 gold/adversarial examples **semantically** (the current unit tests validate schema/fixture integrity, not language understanding). Human-review workflow can remain the primary scoring authority.
3. For full-method comparisons, build a faithful host for **pstack / Matt Skills / FIRST-mode / Neutral** including method-specific skill loading and review/helper stages. Pure prompt proxies are insufficient to rank native approaches. Use the same Ultra/free provider, task, sandbox, evaluator, and fixed resource budget; record helper cost and latency. See [METHOD_COMPARISON_GATE.md](./METHOD_COMPARISON_GATE.md).
4. Freeze and execute scored replications only after these gates pass. No new inference was launched from this V1 replay.
