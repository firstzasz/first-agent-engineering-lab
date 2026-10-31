# NVIDIA-only tool-loop diagnostic V1

**Declared before execution.** This is a distinct diagnostic following V0's transport timeout, NOT a silent retry, NOT a scored methodology run.

- Preserved failed V0 run: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209522589
- Only model/provider: NVIDIA NIM `openai/gpt-oss-20b` (free entitlement as previously demonstrated).
- Only changed experimental parameter: per-request network timeout **50 → 90 seconds**.
- Fixed: same code, synthetic `make_slug` fixture, task, prompts, four allowed tools, total max 9 model requests, 1100 max output tokens/request, grader, hidden tests and no fallback.
- One new independent workspace, no feedback from hidden grader to contestant, no request retry.
- GitHub workflow `.github/workflows/free-agent-loop-nvidia-v1.yml` is research-branch and workflow-file-push scoped. Only trusted branch code gets the NVIDIA Secret at inference step. Separate no-key grading job.
- No Groq, no NVIDIA-hosted DeepSeek, no OpenRouter request in this diagnostic. No merge to main or production code.
- Interpretation: V1 success would demonstrate capability with an extended waiting window, but not establish repeatability or provider superiority. Any failure remains valid evidence.
