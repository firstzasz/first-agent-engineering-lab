# Free-provider API preflight v0 (research-only)

**Status:** prepared on isolated research branch; execution evidence must be read from GitHub Actions, not inferred from file creation.

## Operator scope (2026-10-31)
- **Only:** NVIDIA NIM + OpenRouter free model IDs.
- **Excluded:** Groq; all DeepSeek-family models on NVIDIA NIM (repeated observed timeouts); any paid model/API/fallback.
- **Comparison still required later:** pstack vs Matt Pocock Skills vs FIRST-mode v0, plus neutral control.
- **Secrets (user-reported existing):** `NVIDIA_API_KEY`, `OPENROUTER_API_KEY`. No secret values or other private data in this public repository.

## One-time research probe
Workflow: `.github/workflows/free-api-preflight-v0.yml`. This workflow runs **only** on a push to `research/free-api-preflight-v0` that changes the workflow file. No schedule, PR trigger, or fork secret exposure. It uses GitHub-hosted Python 3.12 with the standard library, read-only GitHub token, no third-party inference gateway, no auto-retry, no model fallback, and exactly two fixed model endpoints:

1. NVIDIA hosted NIM: `openai/gpt-oss-20b` (catalog advertises prototype Free Endpoint).
2. OpenRouter: `nvidia/nemotron-3.5-lightning:free` (the `:free` suffix is compulsory; OpenRouter provider fallback disabled).

Per provider: up to one synthetic `PONG` chat request and one `add_numbers` tool-call probe, `max_tokens=320`, 35-second network timeout. Maximum **4** inference requests total. The tool-call probe detects whether the model emits a named tool call; it does not execute the tool or prove correct arguments, code editing, or task completion. Chat responses may be reasoning-only; inspect the structured result.

## Data and verification
- Secrets are read only at step runtime; prompt and response bodies never appear in logs, outputs, or artifacts.
- `api-preflight-result.json` contains only model/provider ID, HTTP class, response-model ID, usage counts when available, elapsed time, and boolean output/tool indicators.
- GitHub Actions uploads sanitized report; inspect the exact workflow run (status, logs, summary, and artifact).
- HTTP 401/403: credential/entitlement to investigate; 429: `QUOTA_BLOCKED`; 5xx or network timeout: provider issue; HTTP 200 without function call: `TOOL_NOT_CALLED` (not a fully verified tool interface).
- None of this is RelayBoard benchmark evidence. All later scored trials must use fresh, isolated treatment contexts and the frozen independent evaluator.

**No production integration, no main merge, and no EXP-0017 C2 execution.**
