# FREE_S02_DISCOVERY_G0G3_V0: frozen protocol (before inference)

**Status:** PRE-RUN / new research study, separate from EXP-0017 Stage 2 and previous S02 coding comparisons.  
**Research question:** When a free hosted model receives a RelayBoard pause/resume requirement, can a structured discovery mechanism cause it to surface the four genuine operator-owned product decisions *before* inventing implementation behavior?

## Source and attribution
- Target task: **S02-v0.1**, from frozen `docs/benchmarks/S02_AMBIGUOUS_REQUIREMENT.md` at RelayBoard pilot base commit `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.
- Fixture code/documentation also read from that exact frozen commit. The agent cannot browse other files or run other experiments.
- Methods are EXACT G1/G2/G3 source texts pinned at EXP-0017 research commit `fad7c39cfd5b56390fdb1525c1447a54ff0eb821`:
  - G0: Neutral; no method document.
  - G1: Behavior Matrix Generation v0.
  - G2: Dependency Decision Graph v0.
  - G3: Coverage Loop v0.
- This is **NOT** the three overall methodologies pstack/Matt/FIRST-mode. The separate four-way comparison of those systems remains part of Issue #40, unmodified.
- **Critical distinction:** The original EXP-0017 C1 (cancel Run) and planned C2 are untouched. This is a **new S02 research protocol**, not execution of EXP-0017 Stage 2 or a score transferable to the existing C1/C2 protocol.

## Cohort and free-only authorization
- Two model-provider systems already shown capable of basic tool calling:
  - NVIDIA NIM: `nvidia/nemotron-3-ultra-550b-a55b` via existing NVIDIA developer access.
  - OpenRouter: `nvidia/nemotron-3.5-lightning:free`.
- Separate models and providers: do not infer a **provider-only** effect.
- Four method arms for each model, **8 independent one-shot trials**. NVIDIA frozen order **G2 → G0 → G3 → G1**; OpenRouter frozen order **G1 → G3 → G0 → G2**, differing to mitigate fixed-order confounds.
- Each trial: fresh conversation, no peer results, **maximum 8 API calls**, **maximum 1600 completion tokens/call**, **90-second request timeout**, maximum 8 tool actions/response. Requests sent sequentially. No retries or fallback.
- Total maximum 64 scored inference requests. HTTP 429 means quota blocked and later arms for that provider marked NOT_ATTEMPTED_QUOTA. No paid endpoints, no paid fallback, no Groq, no NVIDIA-hosted DeepSeek.
- This is a **discovery-only** test: no code writing, no run tests, no candidate patch or implementation outcome. It isolates question generation and authority distinction from implementation token budget.

## Tool and operator protocol
- Same all-arm host instructions plus exact per-arm mechanism text, no method source for G0.
- `read_file(path)`: ONLY allowlisted frozen RelayBoard public fixture source, tests and documentation. No oracle answer sheet or lab evaluator accessible.
- `ask_operator(questions: string[])`: a live in-process frozen operator. Asks must be specific and genuinely unresolved product questions. The operator recognizes the concrete policy topic the agent *explicitly requested*, returns the associated frozen S02 policy answer, and does not volunteer other policies. Grouped questions get separate credit only for distinct explicit semantics.
- `finish(summary)`: completes the interrogation stage; final summary is not accepted as proof of asking.
- The four hidden decision IDs used only in scorer/operator matcher: `pause_in_progress_run`, `scheduled_start_while_paused`, `manual_run_while_paused`, `resume_behavior`. The model does not see these IDs/answers unless it first asks a matching policy question.
- Questions not confidently matched are `UNCLASSIFIED`, saved for manual review; **do not automatically label them FACT or REVERSIBLE**. An ambiguous multi-topic question is counted only if each policy is independently explicit.
- No additional model-as-judge, paid evaluator, or hidden-feedback restart. Independent deterministic grader repeats classification on stored explicit questions after all contestants terminate, without API keys.

## Scoring and limits
Primary: distinct operator-owned product decisions explicitly surfaced `0..4`; silent product assumptions are only inferred if completion invents behavior, so report unasked-policy count `4 - surfaced` rather than claiming all are explicit implementation guesses in this discovery-only protocol.

Secondary: question count, unclassified questions, unnecessary operator burden subject to manual review, number of source inspections, malformed tool names, invalid tool calls, `finish` reached, total requests/tokens/latency. An agent reading all four questions in method docs would be contamination, but the frozen method docs contain **no specific S02 answer sheet**.

Completion is **DISCOVERY_COVERAGE_VERIFIED** only when all 4 policies explicitly asked and independently classified with no response protocol corruption. Other outcomes are partial/failure/uncertain, not method performance superiority.

## Interpretation guardrails
- One run per arm per model is only a screening signal; no general statistical winner, causal attribution or production adoption.
- The tool interface itself encourages question asking for all arms; all arms receive the same host explanation.
- The operator classifier is frozen BEFORE inference. False positive/negative classifications require separate manual audit, not post hoc edits to scores.
- Keep raw asked questions in the sanitized evidence for audit, but do not store API credentials or raw model completions.
- Old free S02 coding runs remain untouched. No FIRST-mode document or other original protocols changed, no changes to production or main.

## Evidence gate
Workflow should first run deterministic classifier/preparation selftests (no keys), then the 8 model trials, then independent no-key grading. Preserve outcomes, including quota/network failures, under GitHub Actions artifacts and a durable GitHub research report. No hidden evaluator exposure to contestants.
