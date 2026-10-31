# V0 observed execution: free-model real agent tool loop

**Date:** 2026-10-31 UTC. **Outcome:** one VERIFIED, one not verified due transport timeout.

- GitHub Actions run: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209522589
- Exact trigger commit: `b3b30b25ab4d050ae4b87f0437cf70e3a1622022`
- Isolated branch: `research/free-agent-loop-v0`
- Model+provider pairs pinned before execution, no paid model and no DeepSeek/NVIDIA or Groq.
- Artifacts (expire after 14 days):
  - OpenRouter agent output: `13046190177`
  - NVIDIA agent output: `13045673929`
  - Independent grader: `13045323100`

## Results

| Provider | Model | Requests | Read/Edit/Test/Diff via tools | Agent public tests | Independent public tests | Independent hidden tests | Disposition |
|---|---|---:|---|---|---|---|---|
| OpenRouter | `nvidia/nemotron-3.5-lightning:free` | 6 | yes / yes / yes / yes; 5 tool actions | PASS | PASS | PASS | **VERIFIED** |
| NVIDIA NIM | `openai/gpt-oss-20b` | 1 | none; first request timed out | not run | FAIL on unchanged baseline | FAIL on unchanged baseline | **TIMEOUT_OR_NETWORK / NOT_VERIFIED** |

OpenRouter's code also passed source shape, candidate/source SHA checks, diff presence, whitespace checks, and preserved read/write/test/diff trace. NVIDIA was not graded as an implementation failure: no implementation was returned, no tools could be called; the baseline's expected NotImplementedError explains its subsequent failing tests. The run workflow conclusion is failure because the independent grader requires both providers verified.

## What this demonstrates
- **VERIFIED:** One free OpenRouter model completed a real multi-turn coding loop with restricted read, write, executable public tests and git diff, then passed a separate no-API-key evaluator on hidden tests.
- **NOT VERIFIED:** NVIDIA model agent capability. Its earlier 2026-10-31 API preflight (short tool-schema probe) was successful, but a larger first agent request in this v0 run returned `TIMEOUT_OR_NETWORK`. Do not infer model inability, price/billing status, or systematic latency from one timed-out call.
- **NOT MEASURED:** the relative effectiveness of pstack, Matt Skills, FIRST-mode and Neutral; broad model reliability or quota.
- No secret values, prompt completions, arbitrary shell execution or production data were intentionally logged. Two isolated fresh synthetic workspaces were used, one per provider. No merge to main.

## Follow-up policy
A future NVIDIA-only diagnostic **must be a separately declared protocol/version**, not an unrecorded retry inside V0. Preserve the v0 timeout and grader exclusion in all comparisons. A new cohort must freeze the change in timeout/token budget and keep its results separate from v0. Pending EXP-0017 C2 remains out of scope.
