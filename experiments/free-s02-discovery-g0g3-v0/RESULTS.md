# Free S02 G0–G3 discovery-only study: results (historical + validity audit)

Date: 2026-10-31 execution, 2026-11-01 qualitative audit. **Status: EXECUTED; deterministic scorer COMPLETED; SEMANTIC_SCORE_UNRELIABLE.**

### Frozen execution evidence
- Exact run: https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41222993755
- Inference trigger SHA: `940da3a06723e01281b8ac59068f31512981c151`; all jobs (preflight, NVIDIA, OpenRouter, independent-grade) completed successfully, approximately 2026-10-31 17:17 UTC.
- Preserved frozen [protocol](./PROTOCOL.md), independent grader, source oracle matcher, raw synthetic questions in temporary workflow artifacts.
- No paid model calls, NVIDIA DeepSeek, Groq, EXP-0017 C2, main merge or production changes.

### Original automated scores (not semantically corrected)

| Arm | NVIDIA Ultra 550B: decisions / 4 | NVIDIA questions | NVIDIA unclassified | OpenRouter Nemotron Lightning: decisions / 4 | OpenRouter questions | OpenRouter unclassified |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| G0 Neutral | 4 | 13 | 11 | 3 | 13 | 7 |
| G1 Behavior Matrix | 4 | 15 | 10 | 3 | 21 | 16 |
| G2 Dependency Graph | 3 | 19 | 16 | 2 | 2 | 1 |
| G3 Coverage Loop | 3 | 12 | 9 | 3 | 4 | 2 |

- NVIDIA reached automatic 4/4 on G0 in 4 model requests, and on G1 in 8 requests. G2 and G3 each required 8 requests for 3/4.
- OpenRouter reached automatic 3/4 on G0, G1 and G3, 2/4 on G2; all four arms used 8 model requests.
- All eight evidence records are internally consistent with the frozen deterministic matcher. This proves **repeatable scoring logic**, not **semantic classification validity**.
- The graph is a *discovery-only* experiment with `read_file`, `ask_operator`, `finish`; it does not measure code correctness or compare the whole-system pstack, Matt Skills and FIRST-mode approaches.

### Subsequent audit: scoring is unreliable

[Question-by-question no-inference readback](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41224324074) showed both **false-positive and false-negative** question classifications. A full case-indexed explanation is in [SEMANTIC_AUDIT.md](./SEMANTIC_AUDIT.md).

- **False-positive:** NVIDIA G0 and G1 receive `resume_behavior` credit without explicitly asking about missed scheduled tasks catching up after resume.
- **False-negative:** OpenRouter G1 clearly asks whether pending scheduled runs trigger immediately at resume versus the next scheduled cycle, but matcher rejects it.
- **False-negative:** NVIDIA G2 explicitly asks about *manual runs* repeatedly, but matcher misses plural and API-shaped language.
- **Cross-sentence contamination:** question text discussing multiple concepts produces matches for decisions not actually asked.
- `UNCLASSIFIED` is **not equivalent to unnecessary**; additional policies about disabled-vs-paused state, dashboard, idempotence and API shapes may be genuine ambiguities.

Therefore, **do not claim NVIDIA G0/G1 truly achieve 4/4 complete requirement discovery**. Do not claim G3 is best, or that one provider wins based on these automated values. Original numeric scores are retained as historic `FROZEN_MATCHER_SCORE`, with `SEMANTIC_SCORE_UNRELIABLE` flag.

### Proposed next research gate
Before another paid-in-tokens free-model run, create a V1 **semantic adjudication rubric** and deterministic adversarial matcher tests; blind-review *existing* eight question transcripts, labeling decisions explicit/partial/missing and separately classifying other operator burden. Only then judge whether to run replications. Reuse the synthetic fixtures; no production integration.

All outcomes are one-shot per arm and cannot support causal method superiority. This new G0–G3 S02 test is separate from frozen EXP-0017 C1/C2 (Stage 2 not authorized).
