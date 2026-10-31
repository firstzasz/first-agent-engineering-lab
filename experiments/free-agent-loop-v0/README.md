# FREE_AGENT_TOOL_LOOP_V0

**Status:** experimental, non-scored smoke test. Separate from frozen RelayBoard cohorts and EXP-0017.

## Purpose

Establish whether these two *free* hosted models can complete the concrete sequence **read source + tests → edit Python code → run actual executable tests → inspect git diff**, with a per-provider fresh synthetic workspace and restricted native function tools.

- NVIDIA NIM: `openai/gpt-oss-20b`
- OpenRouter: `nvidia/nemotron-3.5-lightning:free`
- Neither Groq nor NVIDIA-hosted DeepSeek is used.
- Existing three-method comparison remains **pstack / Matt Pocock Skills / FIRST-mode**, with **Neutral** as control. This smoke run is not a methodology comparison.

## Source and safety boundary

- `fixture/slug.py` starts with `make_slug` intentionally unimplemented, and `fixture/test_public.py` contains public acceptance tests.
- `evaluator/test_hidden.py` is independent grader-side only, never included in the model's tool-visible workspace.
- The model receives a strict synthetic task; only functions `read_file`, `write_file`, `run_tests`, `show_diff` are exposed.
- `read_file` has an explicit 2-path allowlist. `write_file` can replace only `slug.py`, requires prior reading, has a 5 KB limit and AST shape guard. No arbitrary shell, network or repository browsing tools.
- `run_tests` executes only the frozen public unittest command; environment is cleared of API credentials and user data. The LLM does not receive hidden evaluator failures.
- Network requests are hard-coded per provider; no retries, no model substitution or paid fallback; maximum nine LLM requests per provider, with 50-second per-request timeout. HTTP 429 stops.
- Only synthetic fixture data goes into the inference requests. No production resources.
- Provider Secrets are available only to the corresponding agent step of the GitHub Action. Independent grader job gets **no model API Secrets**.
- No raw model messages, model answer text, raw HTTP errors, secret values or user data are printed. Evidence artifacts contain submitted synthetic code, diff, compact tool event trace, boolean checks, usage counts when available and hash.

**Caveat:** Running any generated source carries risk even with a file allowlist and sanitized subprocess environment. This experiment uses synthetic inputs and a restricted Python AST, not a general-purpose untrusted-code sandbox. It must not be reused for arbitrary user code or production repositories without stronger isolation.

## Workflow and evidence

A dedicated branch-only GitHub Actions workflow `.github/workflows/free-agent-loop-v0.yml` is triggered once on workflow-file push. No schedule or PR-based secret exposure.

Expected artifacts: `agent-loop-nvidia`, `agent-loop-openrouter`, and `free-agent-loop-grade`.

Independent grade checks both code candidate SHA-256s, tool trace, public tests, hidden test cases and the requested workflow. An agent's claim to have finished is not considered verification.

Report successes, quota/timeout/host errors and failures individually. **Do not assign scores to pstack/Matt/FIRST/Neutral from this smoke run.** No merge to main, no EXP-0017 Stage 2, no production integration.

## Next gate

Only if this tool-loop smoke works: freeze a fair matched, evaluator-blind cohort on the same two model/provider configurations, with four methodology arms and predeclared repetition and exclusion rules. Model/host quality should not be confused with methodology effects.
