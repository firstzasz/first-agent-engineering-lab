# Free model S02 four-arm portability screen v0

**FROZEN PRE-RUN**. Pilot only, 8 independent contestant workspaces. No scored run at time of freeze.

Question: Can the two free model-provider systems execute the same frozen RelayBoard S02-v0.1 task under Neutral, the pstack Codex port, the Matt Pocock Codex port, and FIRST-mode v0, when all methods are adapted to a single-agent restricted-tool host?

## Cohort
- Fixed base fixture: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.
- Fixed task: S02-v0.1 (pause/resume). Frozen evaluator and operator answer sheet unchanged.
- Providers: NVIDIA hosted `openai/gpt-oss-20b`, OpenRouter `nvidia/nemotron-3.5-lightning:free`.
- **Only free**. NVIDIA DeepSeek excluded. Groq excluded. No paid fallback, automatic retry or substitutions.
- NVIDIA order: **Matt, Neutral, FIRST, pstack**; OpenRouter order: **pstack, FIRST, Matt, Neutral**. Each run fresh; no previous-run outputs in model context.
- Within each run: **at most 9 inference calls**, 3000 output tokens per call, 90-second HTTP timeout, maximum 12 tool actions per response, at most 6 successful file writes, and one fixed prompt.
- Each provider has a maximum of 36 scored API calls for this cohort. Any HTTP 429 becomes `QUOTA_BLOCKED` for that run; later scheduled arms may be reported `NOT_ATTEMPTED_QUOTA`. No paid fallback.
- One attempt per run; no hidden-evaluator feedback or after-outcome repair.

## Method identity and portability limitation
- Neutral: no injected methodology.
- FIRST: frozen `docs/approaches/FIRST_MODE_V0.md` from the fixed Pilot Start State.
- pstack: frozen `PSTACK_CODEX_PORT_V0.md` from `research/batch-orchestration-round2` (pinned commit `226a03a883c65c81223ca49e00ddd058e1b38691`).
- Matt: frozen `MATT_CODEX_PORT_V0.md` from the same pinned commit.
- The source port documents were designed for Codex with subagent helpers, native skill-file reading, and collaboration question routing. **This pilot does not implement those native capabilities**. A single-agent host-binding note substitutes `ask_operator` for collaboration messages, direct file tools for shell/worktree, and a single implementation/review pass for helpers. Source methodology text remains unedited. Findings must be labeled **non-native portable-proxy results**, not comparisons of full native pstack/Matt systems.
- No methodology injected into other arms. Evaluator cannot change after contestant starts.

## Tool and operator interface
Contestant can list and read only synthetic RelayBoard fixture files plus TASK/METHOD, write only four application files and an optional `tests/test_pause.py`, request test execution in a Docker container with network disabled, see file diff, and ask the frozen operator product questions. No arbitrary shell, other GitHub branches, evaluator files, hidden tests, or secrets tool.
- The oracle is kept in the runner, never delivered to contestant until an explicitly asked and recognized product/preference question. The operator does **not** volunteer unasked requirements.
- Deterministic question classifier maps matching requested decision topics (in-progress Run, missed scheduled start during pause, manual Run during pause, and resume catch-up) to the four frozen answer values. Raw question text and matched categories recorded; uncertain classifications marked `UNCLASSIFIED` rather than guessed.
- Extra FACT/engineering questions are not answered with product policy.
- No causal claim based on one run/arm.

## Security and evidence
- The runner holds only the provider's GitHub Secret. Generated code is executed **only in Docker** with `--network none`, dropped caps, non-root, read-only mounts, no provider keys, and tight resource limits. No arbitrary shell tool offered.
- The independent grader job has **no provider Secrets**; it reads frozen evaluator from lab checkout only after contestant termination, runs code in a separate network-disabled container, and emits public+hidden acceptance.
- Append-only run events contain tool-name/path/status, question and matched product IDs, model response metadata where available, counts and latency, file SHA-256 and git diff. No raw auth keys, raw model completions, raw HTTP error bodies or private data in logs.
- Success levels: `EXECUTED`, `IMPLEMENTED`, `VERIFIED` require independent evaluator evidence; errors and incomplete runs preserved.
- Untrusted code safety remains an experimental research boundary; no FIRST production files/data, credentials or production infrastructure touched.

## Stop and future work
- Stop after all eight dispositions (or quota ceilings); do not silently launch S04, repeat runs, or EXP-0017 C2.
- Publish report and exact links/sha/evidence. These small, 1-run-per-cell results are **screening only**, not robust ranking.
