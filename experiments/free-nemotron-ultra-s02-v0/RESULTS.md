# EXP: NVIDIA Nemotron 3 Ultra free S02 single-agent four-arm screen v0

**Status: EXECUTED + independently VERIFIED for behavior in 2/4 arms; discovery failure in all 4.**

Date: 2026-10-31 UTC. No main merge or production integration.

- Original frozen protocol: [PROTOCOL.md](./PROTOCOL.md).
- Full model+method GitHub Actions run [#41218206140](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41218206140).
- Independent no-inference trace readback [#41218871576](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41218871576).
- Historical GPT-OSS 20B and OpenRouter Nemotron Lightning comparison [#41211207214](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41211207214) and [result digest](https://github.com/firstzasz/first-agent-engineering-lab/blob/research/free-s02-method-screen-v0/experiments/free-s02-screen-v0/RESULTS.md).
- Changed variable: NVIDIA hosted model `openai/gpt-oss-20b` → `nvidia/nemotron-3-ultra-550b-a55b`. Same frozen S02-v0.1, base fixture SHA `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`, workflow-method proxy sources, 9-request cap and 90-second request timeout.
- Free NVIDIA hosted developer endpoint, `NVIDIA_API_KEY` GitHub Actions Secret; no paid fallback. Groq and DeepSeek-NVIDIA excluded.

## Preflight evidence

One unscored API call: HTTP 200, 1.56 seconds. Response model exactly `nvidia/nemotron-3-ultra-550b-a55b`. Returned one valid `list_files` function call. Usage: 627 prompt, 31 completion, 658 total tokens. No output data or key values printed. The model is catalog-listed as a free prototype endpoint. The operator's typical reported 40 RPM limit is not an attested limit for this model or a throughput guarantee.

## Four-arm scores

| Arm | Requests | Tool actions | Changed files | Agent public test invoked | Independent public | Frozen S02 oracle | Product decisions surfaced | Overall |
|---|---:|---:|---:|---|---|---|---:|---|
| Matt non-native proxy | 5 | 4 | 0 | no | PASS (unchanged baseline) | FAIL (pause interface absent) | 0/4 | **HTTP_500 / no implementation** |
| Neutral | 9 | 13 | 4 | no | PASS | PASS | 0/4 | **BEHAVIOR VERIFIED; discovery NOT VERIFIED** |
| FIRST-mode v0 single-agent proxy | 9 | 12 | 4 | yes, at request 9, PASS | PASS | PASS | 0/4 | **BEHAVIOR VERIFIED; discovery NOT VERIFIED** |
| pstack non-native proxy | 9 | 9 | 1 | no | PASS (base behavior) | FAIL (pause interface absent) | 0/4 | **NOT VERIFIED** |

All eight previous S02 GPT-OSS 20B / OpenRouter Lightning cohort runs reached no combined public+oracle acceptance. In contrast, **2/4 Ultra arms** passed combined independent public/frozen evaluator. This is a narrow one-shot observed difference across runs with different calendar time and model/host behavior, NOT proof of model advantage or method causality.

## Detailed trace readback

- **Matt:** four successful HTTP 200 requests then one NVIDIA HTTP 500 on fifth. Four syntactically valid tool actions (three file reads, one list). No write, no test, no question. The failure is transport/provider-level; do not attribute its outcome to Matt's methodology.
- **Neutral:** 9 HTTP 200 requests, 8 reads, 1 list, 4 writes; first write at request 6; four changed files `models.py`, `service.py`, `store.py`, `web.py`. No public-test tool invocation and no operator question. Both independent public and frozen S02 acceptance pass. Approx. 52,276 reported total tokens across requests.
- **FIRST-mode:** 9 HTTP 200 requests, 6 reads, 1 list, 4 writes, 1 actual public-test invocation at request 9, PASS. First write at request 5, same four files changed. Both independent suites pass. Approx. 77,003 reported total tokens across requests. No operator question.
- **pstack:** 9 HTTP 200 requests, 7 reads, 1 list, 1 write, first write only at request 9, so partial implementation. Public suite passes unchanged base behavior, frozen S02 oracle fails. Approx. 46,247 reported total tokens.
- No malformed tool names or denied tools were recorded in these four Ultra traces, unlike some prior NVIDIA GPT-OSS 20B runs. This is an observation from this cohort only.

## Correctness vs requirement discovery vs process

The frozen S02 task intentionally contains four product decisions. **0/4 surfaced in every arm**, and each implementation that passed the frozen evaluator necessarily adopted the oracle-compatible behavior **without asking**: 4/4 silent product assumptions under the frozen discovery metric. Therefore do **not** label Neutral or FIRST as fully successful requirement discovery. They passed *behavior acceptance*, not *operator decision elicitation*.

The observed FIRST-mode process independently used public tests, while Neutral did not invoke public tests in its allotted 9 requests. This is worth replication but insufficient to claim FIRST-mode superiority: one run/arm, different token usage, shared 9-request ceiling, and non-native host.

The run and grader jobs completed successfully because they preserved and evaluated all four dispositions. A green GitHub Actions status does NOT mean all arms passed.

## Interpretation and next research gate

1. The NVIDIA Ultra free model was reachable and supported the fixed tool protocol; 40 RPM alone should not be mistaken for a stable throughput guarantee or unlimited access.
2. **Behavior success 2/4** (Neutral, FIRST), **discovery success 0/4**, **all four full-method comparisons inconclusive**. Frozen evaluator and public suites supply independent executable evidence of behavior for two candidates.
3. Matt's HTTP 500 should remain a separate provider failure, not be silently rerun in this cohort.
4. Proposed next work: freeze a V1 requirement-discovery mechanism and tool-host calibration for `ask_operator` coverage. Perform balanced independent replications under free-only quota, with fidelity controls for pstack and Matt's native subagent/skill mechanisms, before inferring a causal method advantage. Do not unilaterally change FIRST-mode or merge anything into production.
5. Older GPT-OSS 20B and OpenRouter Lightning observations must remain intact. This cohort does not automatically authorize S04 or EXP-0017 C2.

## Evidence artifacts

From run #41218206140, retained for 14 days:
- `ultra-preflight` id `13048749284`;
- `ultra-s02-candidates` id `13048289161`, including candidate fixtures, diffs, tool traces, and hashes;
- `ultra-s02-independent-grades` id `13049256347`.

Independent readback #41218871576 derived all action counts and model/token observations from the frozen cohort evidence. The unabridged artifacts expire: this report is the persistent summary, not a full Git blob archive of their bytes. No API secrets or raw model completions were intentionally logged.
