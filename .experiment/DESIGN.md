# Problem

A failure alert belongs to a terminal failed Run under GLOSSARY.md. The current service emits it on each failed Attempt including Attempts that can retry. The existing retry state and data shape are sufficient. Runtime reproduction proves the alert appears while the Run is still running.

# Usage (caller's view)

POST /api/jobs/daily-report/runs returns a new running Run.
POST /api/runs/run-001/attempts with succeeded false returns retry after the first attempt and failed after the second. GET /api/alerts must show zero alerts at retry and one alert after failure. A second failed Run must add its own alert. A successful retry must add none.

# Shape

Candidate A retains Job, Run, Attempt and Alert dataclasses and the current Store schema. RelayBoardService.record_attempt(run_id, succeeded=...) owns the state transition. Pseudocode is add Attempt, set succeeded and return on success, return retry when below max_attempts, otherwise set failed, emit one alert, return failed. Remove the alert call from the retry branch. The one public operation hides the entire retry and terminal notification policy. No signature changes are required. Model the Domain keeps Run and Attempt separate in the existing state machine. Laziness Protocol makes deletion the preferred change.

Candidate B makes Store.add_alert enforce a unique (run_id, kind) row, through a unique SQLite index and conflict handling. The service retains both existing emission calls. This hides duplicate writes behind the Store API but leaves a terminal failure alert observable for running or ultimately successful Runs. Correcting that still requires service lifecycle policy, which splits ownership across service and storage. A schema alteration increases surface area without addressing the earlier alert.

# Red flag screen and interface depth

Candidate A introduces no shallow module, information leakage, temporal decomposition, pass-through, split ownership, second path, importable internals or hand-synced list. It concentrates policy in the existing record_attempt operation. Existing interfaces do not grow.
Candidate B has split ownership because storage must know alert identity while service still owns terminal outcome. It conceals duplicate insertion but fails the terminal-outcome rule. Schema and insertion APIs would carry more lifecycle detail. It is rejected before synthesis.

# Synthesis decision

Candidate A is the base. Nothing is grafted from B. Removing the premature emission fixes the observed cause and leaves legitimate separate Runs unchanged. A fresh design-choice helper is unnecessary because the public glossary and reproduced early alert rule out B. A fresh implementation helper and a separate review helper remain required.

# Tradeoffs accepted

We accept the existing sequential fixture service contract in exchange for a surgical lifecycle fix. Concurrency, transaction recovery and persistent alert migrations have no observed trigger in this task and are outside the demonstrated mechanism.

# Alternatives considered

Storage deduplication lost because it leaves an incorrect early alert and adds lifecycle knowledge to storage. Deduplication by Job would also suppress legitimate alerts for distinct Runs and cannot satisfy TASK.md.

# Open questions and risks

No unresolved product preference exists. Could a review uncover a public path missed by the regression checks? The fresh scoped review will inspect the service callers and public evidence. No hidden evaluation is available to this run.

# Next implementation step

The bounded helper will write failing WSGI regression tests, run and commit only those tests, then remove the retry-branch emission and rerun the tests.

# Architect phases

1. Ground. Complete in GROUNDING.md.
2. Sketch. Complete with two structurally distinct candidates above.
3. Agree. No opt-in checkpoint requested. Proceed under METHOD.md.
4. Implement. Delegated next.
5. Scrap. Not applicable unless evidence shows the chosen design is wrong.
