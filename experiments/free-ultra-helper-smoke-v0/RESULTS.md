# Ultra Helper Host V0: observed failure (do not erase)

**Date:** 2026-10-31 UTC. **Status:** EXECUTED, NOT_VERIFIED.

- Model and provider: NVIDIA NIM free hosted `nvidia/nemotron-3-ultra-550b-a55b`.
- [Live protocol run #41230556375](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230556375); 4/4 preflight unit tests succeeded; live host step **failed**, independent grader **failed** as intended.
- Exactly **one** API request was sent (Lead), HTTP 200, **6.10 seconds**.
- The model emitted a tool call named `submit_plan` and the response-model ID matched the pinned Ultra model.
- Nevertheless, the returned parsed tool arguments did **not pass** the frozen Lead `plan_valid` check (expected `steps` list length 1–4, all elements strings max 500 characters). The runner stopped. **Implementer and Reviewer were not called.**
- The original run is therefore a **structured function-argument validation failure**, **not** a provider timeout, quota limit, missing credentials, or successful three-role context test. One response does not establish long-term reliability.
- Independent no-Secret grader correctly emitted `LIVE_HELPER_SMOKE: NOT_VERIFIED`, failed multi-role checks and preserved the partial sanitized evidence.
- No model-supplied source was executed or persisted; no production access, no paid fallback, no Groq or DeepSeek-NIM.

## Declared next diagnostic (new branch and protocol)

Change **only the Lead function input schema** from a multistep `steps: string[1..4]` plan to a minimal `ack: true` capability handshake. Keep the same Ultra model, role count, fresh request construction, Implementer patch interface, Reviewer tool, 320-token output cap, 90s request timeout, single attempt per role, no fallback and independent grader. Rename experiment to V1 as metadata.

This tests whether a simpler lead function contract unblocks subsequent roles. It is a separate experiment, **not** a redo or hidden repair of V0. Its success would still not verify native pstack/Matt/FIRST methods.
