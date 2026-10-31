# Free Ultra helper roles V1: separately frozen diagnostic

**Status:** pre-execution protocol, new research branch. V0 failed at lead `submit_plan` argument validation on a successful HTTP 200; [V0 evidence](https://github.com/firstzasz/first-agent-engineering-lab/blob/research/free-ultra-helper-smoke-v0/experiments/free-ultra-helper-smoke-v0/RESULTS.md).

**One functional change:** Reduce the **Lead function-tool schema** from structured `steps` list (1–4 strings) to a single required boolean `ack=true` to distinguish schema complexity from the underlying three-role host capability.

**Held fixed:** NVIDIA free Ultra `nvidia/nemotron-3-ultra-550b-a55b`, synthetic task, Lead/Implementer/Reviewer fresh contexts, Implementer `submit_patch` source schema, Reviewer `submit_review` read-only schema, 3 total requests (one each), max 320 output tokens/request, 90s timeout, no retries or paid fallback, no other provider, no model-produced source execution, sanitized artifact and independent no-Secret grade. Only version labels change for provenance.

**Question:** Does simplifying the Lead tool arguments unblock the implementer and reviewer session protocol? Success would be a narrow host-capability smoke, not proof of real native pstack/Matt/FIRST workflow fidelity or coding correctness.

**Stop rule:** Any failed role/tool stops the run, preserves evidence, and receives NOT_VERIFIED. No automatic V2 or budget expansion. No EXP-0017 C2, no main branch merge, and no production changes.
