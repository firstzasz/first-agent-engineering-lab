# Mock Helper Host: safety-contract calibration V0

**Executed:** 2026-10-31 UTC, research branch only. **18/18 offline tests PASS in latest corrected run.**

- [Latest GitHub Actions run #41230351423](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230351423): 18 tests passed; question V1 replay also completed with all 8 source anchors valid.
- An earlier host attempt [#41230317054](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230317054) failed eight tests with a Python set/dict comparison error; fixed in host code and preserved as an observed implementation failure.
- [Original V1 selftest #41230079816](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230079816) failed one test-fixture rationale length assertion; this too remains visible.
- No inference requests, NVIDIA/OpenRouter API Secrets, model outputs, or production data used in host-calibration tests.

## Implemented and tested

The synthetic `helper_host_contract.py` and `test_helper_host_contract.py` exercise:
- distinct lead/implementer/reviewer **fresh context** lifetimes, without parent chat history copying;
- explicit read-file and role-based tool permissions; reviewers cannot write;
- synthetic helper writes affect only its own snapshot, never another reviewer or the base fixture;
- hidden evaluator/oracle files cannot be placed in scope or read;
- a **shared** total request and token budget across lead, implementer and review contexts, with hard caps;
- method stage coverage requires host evidence; merely including a method document never validates execution;
- fake `run_public_tests` explicitly returns `real_tests_executed=False`, so the synthetic host cannot claim actual code verification.

## Interpretation

**VERIFIED:** the mock Python safety/accounting contract passes 9 host unit tests plus 9 semantic-evidence unit tests, total 18/18.

**NOT VERIFIED:** actual NVIDIA/ OpenRouter helper API calls, live worker context isolation, real native pstack/Matt skill invocation, real Docker execution of untrusted model-written code, integration of the helper sandbox with the existing S02 harness, method-specific reviewer quality, or a full end-to-end comparison. These are deliberately not inferred from mock success.

**Next gate:** implement an actual model adapter that logs child-session calls and shares the total budget while preserving the source-specific pstack/Matt skill routing. First run a *synthetic non-scored capability smoke* and verify host event traces; only then freeze full-method S02 and S04 scored cohorts. See [METHOD_COMPARISON_GATE.md](./METHOD_COMPARISON_GATE.md).
