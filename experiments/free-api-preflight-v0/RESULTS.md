# Free API preflight v0: first observed execution

**Status:** VERIFIED for narrow API connectivity + tool-call-name emission; **not** a RelayBoard engineering benchmark.

- UTC date: 2026-10-31
- Trigger: isolated research branch workflow-file push only
- Workflow run: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41208669287
- Trigger commit: `9db940e4aa8c3d7db46ce4783e309c26c7b8e919`
- GitHub Actions outcome: **success**
- Test job: `free-provider-smoke` / `124558887450`, completed success
- Sanitized result artifact: `free-api-preflight-report`, artifact ID `13045446677` (14-day retention)
- Test input: synthetic `PONG` chat request + `add_numbers(a=2,b=3)` function-call instruction; no production data, no LLM benchmark tasks
- Max requests authorized by code: 4; observed: 4

## Observations from independent GitHub job log

| Provider | Fixed model ID | Mode | HTTP | Elapsed (seconds) | Model emitted content? | Named tool call? |
| --- | --- | --- | --- | ---: | --- | --- |
| NVIDIA NIM | `openai/gpt-oss-20b` | chat | 200 | 1.97 | yes | no |
| NVIDIA NIM | `openai/gpt-oss-20b` | tool | 200 | 4.48 | no | yes |
| OpenRouter | `nvidia/nemotron-3.5-lightning:free` | chat | 200 | 2.07 | yes | no |
| OpenRouter | `nvidia/nemotron-3.5-lightning:free` | tool | 200 | 0.70 | no | yes |

Both configured Secrets were *operationally* accepted by the corresponding provider. No secret values appeared in the probe's intended printed output. DeepSeek NVIDIA and Groq were not called. Free-only OpenRouter model ID is pinned with `:free`, and `provider.allow_fallbacks=false`; there is no client-side paid fallback or retry.

## Interpretation
- **VERIFIED:** HTTPS access, authentication success, nonempty chat content, presence of a function call with the expected function name from each model, and a successful GitHub-hosted workflow.
- **NOT VERIFIED:** semantic tool argument correctness, multi-turn tool execution, agent planning/coding, consistent latency, provider reliability under repetitions, exact account quota limits, real-time billing ledger, model quality, or the comparative effectiveness of pstack/Matt/FIRST-mode/Neutral.
- **Historical observations only:** the timings above are from a single attempt each and must not be treated as throughput benchmarks.
- **Remaining plan:** construct a properly controlled agent harness, validate tool arguments and tool-execution loops with synthetic fixtures, then freeze the matched four-arm comparisons using these free providers only. No paid model and no NVIDIA-hosted DeepSeek.

## Reproducibility/safety
Workflow source: `.github/workflows/free-api-preflight-v0.yml`, script: `experiments/free-api-preflight-v0/preflight.py`. Workflow has no schedule/PR trigger and the branch/path-limited push trigger; `main` is unchanged. Keys are injected from repository Actions Secrets at runtime and never committed. Result artifact is sanitized and temporary. Any rerun is a new experiment execution and must obey free-tier quota controls.
