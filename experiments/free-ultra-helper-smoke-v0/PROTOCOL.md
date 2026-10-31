# Free NVIDIA Ultra helper-session API smoke v0: frozen protocol

**Non-scored, synthetic-only host capability check. Not a four-method benchmark.**

## Question
Can the same free hosted NVIDIA Nemotron Ultra model complete **three real independent model-request contexts** (Lead, Implementer, Reviewer) with syntactically valid role-specific function calls, sharing one hard call budget, without the Lead's private marker being copied into the other model requests?

## One-shot execution
- Model (pinned): `nvidia/nemotron-3-ultra-550b-a55b`; NVIDIA direct free developer endpoint with `NVIDIA_API_KEY` runtime GitHub Actions Secret.
- Exactly **3 sequential inference requests**, at most one per role. Each request max output `320` tokens and network timeout `90` seconds, with no retry, no fallback, no paid endpoint. Free-tier limit and quota can vary. HTTP 429 stops.
- Each request has a **fresh two-message context** and **only its matching function tool**. Lead may `submit_plan` (does not write files), Implementer may `submit_patch` (returns one synthetic function source), Reviewer may `submit_review` (read-only boolean and reason code).
- No actual nested native agent API exists. Orchestration of three fresh requests is the *host emulation* of helper sessions; do not call this Cursor or Claude subagent equivalence.
- Lead system prompt contains unique marker `LEAD_ONLY_SYNTHETIC_SCOPE_MARKER_7X9`; neither other request may contain that literal marker. Do not pass Lead's raw response into Implementer or Reviewer. Reviewer receives only the Implementer patch after syntax and allowlist checks.
- No code from the model is executed in the credential-bearing step; only AST parser and source-shape validation. No arbitrary shell, network or file browsing offered to the model.
- Whole test case is a synthetic one-function string normalization task, with no business, user or production data.
- Per-run hard total request cap 3; token usage is recorded if returned, and expected request payload size bounded. Every call counts toward the same ledger, including Reviewer. No hidden free-tier upgrade or model change.

## Evidence
- Sanitize everything in public GitHub logs/artifacts: provider model ID, role, request count, response status/latency, tool call name validity, prompt structure count, marker presence boolean, output hashes and usage counters. **Never log or persist API key or raw model completions/code.**
- Independent no-Secret grader checks the evidence manifest for 3 distinct sequential roles, proper tool names, absence of marker outside Lead, request cap, model ID, JSON schema, and recognized host statuses. This validates **reported host behavior**, not crypto-verifiable message isolation, code correctness or reviewer quality.
- Preserve the previous 18/18 mock-host unit-test evidence. This is a **live API host smoke**, not proof that pstack, Matt and FIRST full workflows were invoked or compared.
- Retain failure cases and stop without fallback; no scored S02/S04/EXP-0017 C2, no merge to main or production.

## Interpretation
Success would establish one proof-of-connectivity of sequential role-separated model requests under a shared host budget. It would not establish native multi-agent parity, long-term reliability, independent high-quality review, ability to fix actual RelayBoard code or comparative engineering-method superiority.
