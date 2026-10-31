# Post-run semantic audit of frozen S02 question grader

**Research-only diagnostic, 2026-11-01. Not a change to the frozen score.**

## Evidence examined
- Original inference / independent deterministic grade: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41222993755
- Full synthetic question readback, without model inference: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41224324074
- Methodology and automatic matcher frozen before running; G0–G3 are mechanisms, NOT the whole-method pstack/Matt/FIRST/Neutral comparison.
- The original machine scores, `discovery-independent-grade` artifact (ID `13051160391`), raw question artifacts (NVIDIA `13051270203`; OpenRouter `13050134294`), and run logs are preserved, not rewritten.

## Automatic grade (unchanged historical evidence)

| Provider | G0 | G1 | G2 | G3 |
| --- | --- | --- | --- | --- |
| NVIDIA Ultra 550B | 4/4 | 4/4 | 3/4 | 3/4 |
| OpenRouter Nemotron Lightning | 3/4 | 3/4 | 2/4 | 3/4 |

All eight records passed deterministic **evidence integrity / scorer consistency**, but this is **not proof the scorer correctly identifies semantic questions**.

## Critical measurement defects

### False-positive: resume catch-up policy inferred from a non-catch-up question
- NVIDIA **G0 question 1** asks whether manual runs are blocked during pause, with incidental wording *"until it is resumed"*. The scorer credits **`resume_behavior`**, despite the question never asking whether *missed scheduled starts are caught up after resume*. It also credits `scheduled_start_while_paused` despite the task already explicitly saying scheduled work must not start during pause.
- NVIDIA **G1 question 1** similarly asks only scheduled versus manual blocking but was credited **all four frozen decision IDs**. This is demonstrably too permissive: it did not ask about in-progress Runs or missed scheduled start catch-up. Its later question 3 does explicitly ask about in-progress Runs, but **no G1 question clearly asks catch-up versus future-only scheduling**.
- OpenRouter **G3 question 4** is a four-part batched question that discusses endpoint response formats and dashboard but does not ask missed-schedule catch-up; it nevertheless gets `resume_behavior` based on superficial mentions of pause/resume endpoints.

### False-negative: clear product policy questions the scorer misses
- NVIDIA **G2 questions 6, 8, 15, 16, 18** explicitly ask whether manual runs remain allowed while paused. The scorer marks them **unclassified**, mostly because its regex matches the singular token `run` rather than plural `runs`, or fails on API-shaped phrasing.
- OpenRouter **G1 question 3** asks: *"When a paused Job resumes, should immediately pending scheduled runs be triggered, or only on next normal schedule cycle?"* This is a direct question about catching up missed scheduled work versus future-only scheduling, but the scorer records **unclassified**. Multiple G1 repeats of that question are also unclassified.
- OpenRouter **G3 question 3** explicitly asks whether `begin_manual_run` remains allowed while paused and is unclassified because the matcher does not recognize identifier-shaped action names.

### Prompt-fact leakage into 'discovered' decision credit
The frozen task already states **a paused Job must not start normal scheduled work until resumed**. The real unresolved product decision is whether *scheduled triggers during pause are discarded or queued*. A question asking only "block scheduled vs manual?" does not demonstrate discovering this **skip vs queue** policy. The matcher frequently awards `scheduled_start_while_paused` credit anyway.

### Other methodological limitations
- A question about **retrying an already-running Run** is related but not identical to "does the existing Run itself continue or get canceled?" Such answers require semantic inspection.
- Questions about dashboard pause state, enabled/paused orthogonality, idempotence and API response shape may be valid additional product requirements, facts, or implementation choices. An `UNCLASSIFIED` tag does **not** prove the question is unnecessary.
- Long batch questions contain distinct semantic decisions. Regex on the concatenated text can produce accidental cross-sentence matches; grouped credit requires individually explicit choices.
- Some methods asked the *same* question repeatedly. Unique decision coverage and operator interruption burden must be measured separately.

## Implication for findings

**The automatic 4/4 values for NVIDIA G0 and G1 cannot be reported as semantically validated full coverage.** Likewise the automatic 3/4 for OpenRouter G1 may be an underestimate, since it explicitly asked a resume catch-up question that the frozen matcher missed.

This semantic audit is **post hoc, qualitative and not blinded to arm identity**. Do NOT replace machine scores with subjective counts and claim a new calibrated winner. Instead report the machine scores as `FROZEN_MATCHER_SCORE`, flag `SEMANTIC_SCORE_UNRELIABLE`, and preserve raw questions for a future independently reviewed adjudication.

## Recommended next controlled gate (proposal, NOT executed)

1. Design a separate **V1 scoring rubric** anchored to each of the four operator-owned decision *contrasts*, not just words: running continuation/cancellation, missed scheduled start skip/queue, manual start allow/block, missed-work catch-up/future-only. Award credit only when both the event context and unresolved alternative are explicit.
2. Include positive/negative and cross-sentence adversarial fixtures for each of the 4 decisions. Test plural nouns, WSGI paths, code symbols like `begin_manual_run`, and repeated/combined questions.
3. Run blind independent manual adjudication of the **existing** question transcripts before new inference; disagreements become `AMBIGUOUS`, never silently resolved in favor of any model.
4. If a model comparison is still warranted, freeze a new V1 cohort that uses the same operator decisions and scorer. Keep original results as historical only.
5. Avoid unverified ranking, automatic graduation of G0/G1/G2/G3, FIRST-mode changes, EXP-0017 C2 or production integration.

This is a **scoring-validity finding**, not proof of a model or methodology win. Public repo contains only synthetic experiment material.
