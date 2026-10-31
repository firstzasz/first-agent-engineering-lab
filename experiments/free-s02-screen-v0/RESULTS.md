# Free S02 Four-Arm Single-Agent Portability Screen v0: final result

**Date:** 2026-10-31 UTC  
**Status:** EIGHT RUNS EXECUTED, INDEPENDENTLY GRADED. No run achieved both public and frozen evaluator acceptance.  
**Inference run:** https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41211207214  
**Forensic trace readback (no new inference):** https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41211720582  
**Targeted public regression diagnostics (no new inference):** https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41211814685  
**Pre-run protocol:** [PROTOCOL.md](./PROTOCOL.md)  
**Branch:** `research/free-s02-method-screen-v0`, not merged to main.

## What was actually tested

Two explicitly free model+provider systems:
- NVIDIA NIM: `openai/gpt-oss-20b`;
- OpenRouter: `nvidia/nemotron-3.5-lightning:free`.

Each model tested **Neutral**, **pstack pinned Codex-port source**, **Matt Pocock pinned Codex-port source**, and **FIRST-mode v0**, in a bounded single-agent tool host. There were 8 independent fresh workspaces on the frozen RelayBoard S02-v0.1 scenario, source base `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.

IMPORTANT: The host is a **non-native single-agent proxy**, not equivalent to the native pstack/Cursor or Matt/Claude Skills workflow, and does not faithfully implement Codex helper-subagent parts of the frozen ports. Therefore findings cannot rank those complete methodologies. No Groq, NVIDIA DeepSeek, paid fallback or frontier-model execution occurred.

## Independent acceptance, discovery and execution

| Provider | Arm | API req | Tools called | Changed source files | Operator decisions surfaced | Public tests | Frozen S02 evaluator | Combined verification |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| NVIDIA | Matt proxy | 9 | 8 | 0 | 0/4 | PASS (unchanged base) | FAIL (pause interface missing) | NOT VERIFIED |
| NVIDIA | Neutral | 9 | 9 | 2 | 0/4 | PASS | FAIL (pause interface missing) | NOT VERIFIED |
| NVIDIA | FIRST proxy | 9 | 8 | 0 | 0/4 | PASS (unchanged base) | FAIL (pause interface missing) | NOT VERIFIED |
| NVIDIA | pstack proxy | 9 | 9 | 1 | 0/4 | FAIL | FAIL; evaluator did not return normal failure list | NOT VERIFIED |
| OpenRouter | pstack proxy | 9 | 15 | 3 | 0/4 | PASS | FAIL (pause interface missing) | NOT VERIFIED |
| OpenRouter | FIRST proxy | 9 | 9 | 2 | 0/4 | PASS | FAIL (pause interface missing) | NOT VERIFIED |
| OpenRouter | Matt proxy | 9 | 15 | 4 | 0/4 | **FAIL** | **PASS** | NOT VERIFIED |
| OpenRouter | Neutral | 9 | 9 | 2 | 0/4 | PASS | FAIL (pause interface missing) | NOT VERIFIED |

All eight trials exhausted the frozen per-run **9 API request cap**, none called `ask_operator`, and none finished with passing agent-side public tests. Six of eight passed the independent public fixture suite, often simply because the original base behaviors remained unchanged. One of eight passed the frozen S02 hidden oracle, but it regressed a separate public behavior.

These are actual execution/independent grading observations, not claims about the full methodology's quality.

## Diagnosed failures and tooling evidence

### NVIDIA model/tool interface
- Matt tool names included literal malformed names such as `list_files<|channel|>commentary` and `run_public_tests<|channel|>json`. Two actions were rejected as `UNKNOWN_TOOL`; two file reads were denied. No valid write/test completion.
- FIRST also produced a malformed `list_files<|channel|>json` call and no write/test completion.
- pstack produced a malformed `read_file<|channel|>commentary` call; made one partial code file change. Its public suite had five runtime errors.
- Neutral changed two source files, but never reached test execution or defined the required pause interface.
- All NVIDIA runs used 9 requests, with a total of 0 valid operator product questions.

### OpenRouter agent control
- Tool invocations were structurally more consistent in this limited observation. The pstack proxy produced 15 tool actions including a `WRITE_DENIED`, changed three files but did not implement the pause API surface.
- Matt proxy produced 15 tool actions, changed four files and called public tests once. It passed the frozen S02 evaluator but failed the public dashboard test.
- FIRST proxy and Neutral changed two files each, without asking product decisions or calling the public test tool before the request cap.

### Exact public regression surfaces
- OpenRouter Matt: `test_public.RelayBoardPublicTests.test_dashboard_has_jobs_table` produced an error. This means its frozen S02 oracle PASS must **not** be counted as a successful end-to-end feature implementation.
- NVIDIA pstack: runtime errors in all five public fixture tests: dashboard, API run/attempt creation, scheduled-run disabled check, disabled-job/manual-run check, and single-attempt alert check.
- The test IDs are verified in the offline forensic diagnostic workflow. The specific exception root causes are **not independently established** in this report.

## Valid interpretations

1. **Demonstrated:** both free providers can complete a simple read/edit/test/diff smoke task under the earlier separate benchmark; the larger S02 task did not reach combined acceptance within 9 requests.
2. **Demonstrated:** external public regression tests catch a failure that the S02 hidden oracle alone accepted, making independent multi-surface validation necessary.
3. **Demonstrated:** malformed tool-action names are a real issue for NVIDIA GPT-OSS 20B in this host/model combination; this is not evidence of poor underlying reasoning by itself.
4. **Demonstrated:** the nine-request cap constrained all eight runs; seven did not invoke test tools at all and none asked the four important product decisions.
5. **NOT demonstrated:** which of pstack, Matt Pocock Skills or FIRST-mode is superior; whether any model can succeed given a larger budget, corrected tool adapter, or native host; reproducibility across seeds/times; or impact of model capability versus methodology.

## Research shortcomings and next experiment proposal

Do **not** retroactively revise this run. Freeze a new V1 protocol only after fixing methodology/tool host fairness:

- preflight multi-turn tool names, tool arguments, and denial/recovery behavior with each free model;
- add one constrained public acceptance diagnostic earlier in the run and measure time-to-first-test;
- increase request budget in a declared, quota-aware, non-adaptive fashion (e.g. 18 or 24 turns) and explicitly cap the number of trials to stay under free daily quotas;
- separate **method fidelity** from tool/host reliability: native pstack and Matt Skills subagent/skill invocation is not represented by this single-agent proxy;
- preserve an operator decision-elicitation mechanism that does not leak answer options before the question, audit question classification against frozen product decisions;
- add dashboard regression to an **independent** acceptance suite for future scenario versions, without changing the frozen S02-v0.1 benchmark;
- run independent replicates only after a clean agent-harness calibration; do not declare a winner from this single-shot screen.

Free API quotas and actual provider entitlement must be rechecked before any further LLM run. Do not launch another batch merely because this one failed. Preserve the observed failure and avoid silent retries.

## Evidence preservation

- Candidate artifacts and sanitized traces are retained in GitHub Actions for 14 days, not permanently. Workflow artifact IDs: NVIDIA `13046585733`, OpenRouter `13046318364`, independent grades `13046293476`.
- Durable narrative and run identifiers are preserved in this research branch and Issue #40.
- No secret values or raw completions were intentionally logged; independent grader ran without model API keys.
- Repo main, FIRST-mode frozen original and older benchmark evidence remain unchanged.
