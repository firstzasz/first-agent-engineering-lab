# S02 Semantic Adjudication V1: reviewer rubric

**Status:** V1 *post-hoc*, separately versioned, **NOT** the original frozen evaluator. Applies only to synthetic S02 discovery transcripts. It must never rewrite V0 scores. No paid or free model inference is needed.

## Four operator-owned *contrasts*

| ID | Minimum to grant EXPLICIT credit | Examples that do NOT receive full credit |
|---|---|---|
| `pause_in_progress_run` | Ask the fate of an **already executing Run** when its Job is paused: continue, cancel, suspend, or otherwise alter existing run lifecycle | Merely ask whether new runs are allowed, whether a retry counter persists, or how to handle pause API with no active Run |
| `scheduled_start_while_paused` | Ask what happens to a **schedule trigger that falls during pause**: skip/drop vs enqueue/defer/replay/pending, or an equivalent distinction | Repeating the prompt's known fact that new scheduled work should be blocked during pause; compare scheduled versus manual starts only |
| `manual_run_while_paused` | Ask if a **manually initiated run can start during pause**: allow vs block, including `begin_manual_run` and plural `manual runs` | Ask where to persist paused state or whether a user can call the pause endpoint |
| `resume_behavior` | Ask whether **scheduled occurrences missed while paused** are made up on resume vs ignored with future-only scheduling (equivalently 'run pending jobs immediately vs next normal scheduled cycle') | Incidental words 'resume'/'unpause'; API response/status; resuming an already executing run; idempotent resume |

## Three-valued labeling

- `EXPLICIT`: a directly requested unresolved product-policy contrast is present in an actual `ask_operator` question; one credit per ID across all questions in a run.
- `PARTIAL`: the same domain is discussed but the distinction above is absent or ambiguous. **Zero primary credit.** Such cases must be reviewed, not assumed missing or credited.
- `ABSENT`: no question in the run requests that contrast. **Zero credit.**
- `NOT_ADJUDICATED`: no usable evidence or review unavailable; do not score as zero.

For any `EXPLICIT`, save the question's **1-based original index and an exact evidence substring**. Treat index as untrusted until an independent artifact-replay script verifies it against the original question. A compound question earns two credits only when the two contrasts are separately and concretely asked, not merely because topic words co-occur in the entire string. Duplicates count as extra operator burden, not extra coverage.

## Authority and limits

Reviewers must separately note FACT lookup burden, reversible engineering choice burden, repeated questions and other possibly legitimate product questions. An 'unclassified' V0 matcher output is **not evidence that a question was useless**. The V1 primary outcome concerns four frozen oracle contrasts only.

This initial retrospective annotation was created after reading method-labelled logs and is **UNBLINDED** and single-reviewer. Even if replay validates every quote, the verdict remains **PROVISIONAL_UNBLINDED**, not a blinded independent semantic evaluation or a basis for ranking methods. For blinded adjudication later, first anonymize and shuffle runs with stable blinded IDs, recruit two independent reviewers, then adjudicate disagreements without changing their original marks. No fresh inference is necessary.

**Validation:** source-anchoring, schema integrity, reproducibility and the difference between frozen V0 values and new provisional judgments can be VERIFIED by executable code. Semantic truth of subjective labels cannot be verified by this replay alone.

## Data protection and experiment isolation

Only synthetic questions from GitHub Actions run `41222993755`. No secrets, raw model answer bodies, user files or production sources. Keep V0 machine scores and their failings untouched. This isn't EXP-0017 C2 and isn't yet pstack vs Matt vs FIRST-mode end-to-end.
