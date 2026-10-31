# NVIDIA diagnostic V1: independently verified tool-loop outcome

**Date:** 2026-10-31 UTC

This is a separately frozen, one-variable diagnostic run following V0's timeout, not an unlogged retry and not a scored methodology comparison.

- Run: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209804076
- Triggered at: `dfce07c116cf287c2881901cc0200dc54f0d0d31`
- Agent job: `nvidia-agent`, **success**; independent grader job: `independently-grade`, **success**.
- NVIDIA model: `openai/gpt-oss-20b`, free hosted NIM endpoint.
- Exactly one declared parameter changed relative to V0: request timeout `50s -> 90s`.
- Requests: **7**; successful tool actions observed: **7**; final status: `TOOLS_COMPLETED`.
- The model read both permitted files, wrote a new `slug.py`, ran public executable tests, and inspected actual Git diff. It was not given evaluator-only tests.
- Final tool checks: read both PASS; write PASS; test used PASS; test passed PASS; diff seen PASS; final public tests PASS; diff whitespace check PASS.
- Independent grader: source-shape safety PASS; candidate/baseline SHA-256 PASS; changed source PASS; tool trace PASS; request cap PASS; patch present PASS; independent public tests PASS; **independent hidden tests PASS**; V1 protocol delta valid.
- Evidence artifacts (temporary 14-day retention): `agent-loop-nvidia` id `13045543040`; `nvidia-v1-grade` id `13045896587`.

## Cross-provider smoke summary

| Provider | Model | Run | Status | Requests | Tool actions | Public test (independent) | Hidden test (independent) |
|---|---|---|---|---:|---:|---|---|
| OpenRouter | `nvidia/nemotron-3.5-lightning:free` | [V0](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209522589) | **VERIFIED** | 6 | 5 | PASS | PASS |
| NVIDIA NIM | `openai/gpt-oss-20b` | [V0](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209522589) | **TIMEOUT / NOT_VERIFIED** | 1 | 0 | baseline FAIL | baseline FAIL |
| NVIDIA NIM | `openai/gpt-oss-20b` | [V1](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209804076) | **VERIFIED** | 7 | 7 | PASS | PASS |

## Interpretation boundaries

The smoke-test capability of both free models is now evidenced, but comparing 6 versus 7 requests or tool actions is **not** a fair speed/efficiency conclusion because the runs use different providers and NVIDIA V1 has a different timeout budget. Preserve NVIDIA V0 as a failure, do not silently erase it.

Neither provider has yet passed a complex frozen RelayBoard S02/S04 run under the four methodology arms. Results do not rank pstack, Matt Pocock Skills or FIRST-mode; those are the **next controlled experiment**, with a Neutral control, strict free-provider scope, independently verified outcomes and separate source/evaluator workspaces.

No Groq, NVIDIA DeepSeek, paid model, production endpoint, or main-branch merge was used.
