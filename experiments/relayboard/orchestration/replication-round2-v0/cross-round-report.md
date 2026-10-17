# Benchmark Replication Round 2: cross-round report

Status: **FINALIZED**. All twelve Round 2 dispositions are durable: **11 evaluated PASS, 0 evaluated FAIL, 1 excluded INVALID_HOST_FAILURE**. Four resumed runs—P-S01-002, N-S04-002, N-S02-002 and N-S01-002—each passed the independent public rerun and unchanged frozen evaluator. P-S02-002 was not restarted.

This report distinguishes observations, replicated signals, hypotheses and unsupported conclusions. It assigns no aggregate methodology score and no universal winner.

## Design and evidence boundary

Round 1 has 11 valid evaluated PASS runs (including the earlier independently evaluated N-S01-001) and one excluded CONTAMINATED run, P-S04-001. Round 2 has 11 valid evaluated PASS runs and one excluded host failure, P-S02-002. There are **10 valid matched treatment/scenario pairs**; all ten pass public and evaluator acceptance in both rounds. An excluded run is not an acceptance failure and is not replaced by another run.

Round 2 is an independent replication, not a retry of Round 1. Its exact reverse execution order was frozen before the first contestant at `b9c7da1e8cb797f49d86e46b229d21e9493b483f`; see [execution order](./execution-order.json). The fixed order was followed, including disposition of the host failure before P-S01-002. Only one contestant run was active at a time.

All runs retain Pilot Start State v0.1 `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`, S01-v0/S02-v0.1/S04-v0, unchanged [scoring](../../../../docs/benchmarks/SCORING_V0.md) and [evaluator protocol](../../../../docs/benchmarks/EVALUATOR_PROTOCOL_V0.md). The unchanged evaluator blob is `3aaaa9924f09ba18a5888d94373a9edc04187926`. FIRST receives the exact frozen FIRST_MODE_V0.md; Matt and pstack reuse the byte-identical pre-outcome Codex ports at `311871987a48a072e36f434e199b1cb28563c81b`. Those ports are explicitly non-native.

Fresh leads/helpers requested `gpt-6.1-sol` / `high` and `fork_turns=none`; runtime model/reasoning identity is independently unverified. Contestants received only assigned packets. Operator responses supplied only asked frozen product semantics. Completed lead/helper contexts were observed before exact candidate freeze and separate evaluation. No hidden result was returned to a same-run contestant. Candidate PRs target their treatment branches and remain draft/unmerged.

Isolation is procedural. Broad tools and a shared filesystem remained technically available. Reports, available action/path evidence and immutable packets were checked, but no complete host access trace proves absence of every possible access. The [final audit](./final-audit.json) verifies remote refs, frozen inputs, protected Round 1 evidence, order, phase boundaries and eleven candidate trees/PRs. Local archived run material and evaluator copies were removed before each subsequent delivery.

## S01: overhead stability

**Observation.** All four arms produced the same application diff in both rounds: one heading replacement in `relayboard/web.py`, 1 insertion / 1 deletion. All eight S01 outcomes passed public and evaluator acceptance. No S01 product question was observed in the three Round 1 batch runs or any Round 2 run; the original N-S01-001 operator history is unknown.

| Treatment | Helpers R1 → R2 | New process files R1 → R2 | Process blob bytes R1 → R2 | Local commits, including start, R1 → R2 |
| --- | --- | --- | --- | --- |
| FIRST-mode v0 | 0 → 0 | 7 → 11 | 12,612 → 16,367 | 3 → 3 |
| matt-codex-port-v0 | 2 → 2 | 18 → 18 | 27,651 → 29,648 | 3 → 3 |
| pstack-codex-port-v0 | 1 → 1 | 30 → 14 | 49,783 → 21,414 | 3 → 3 |
| Neutral | unknown → 0 | unknown → 1 | unknown → 5,317 | unknown → 3 |

“Process files” are newly added `.experiment/`, `.scratch/` and `REPORT.json` blobs, excluding the prepared packet. Bytes measure stored Git blobs, including compressed/binary artifacts. Feature documentation, production and test changes are tracked separately. Evidence packaging and the common reporting envelope affect these counts; a file is not a standardized unit of work or a quality score.

**Replicated signal.** The implementation scope stayed minimal. FIRST used no helper, Matt used two fresh reviewers, and pstack used one fresh reviewer in both rounds. Among the three method arms with comparable process records, both ports produced more process files/bytes than FIRST in each round.

**Non-replicated signal.** Absolute artifact volumes and the Matt-versus-pstack footprint ordering were not stable: pstack had more process files than Matt in Round 1, fewer in Round 2. A two-round Neutral overhead comparison cannot be established because the original trace is missing. Stable commit counts do not imply equal work.

Recorded preparation-to-freeze seconds were FIRST 167.560 → 209.788, Matt 7,522.340 → 403.367, pstack 406.021 → 648.520, and Neutral unknown → 125.583. These times include host, operator and archival delays, and do **not** establish model compute speed or methodological latency. Full tool/action counts, tokens and cost remain unknown.

Evidence: [S01 metrics](./cross-round-metrics.json), [F-S01-002](./results/F-S01-002/run.json), [M-S01-002](./results/M-S01-002/run.json), [P-S01-002](./results/P-S01-002/run.json), [N-S01-002](./results/N-S01-002/run.json).

## S02: requirement-discovery stability

**Observation.** Every completed S02 run passed acceptance. Discovery is scored separately: a correct unasked product choice still counts as a silent assumption under the frozen rubric.

| Treatment | Decisions surfaced / 4, R1 → R2 | Silent assumptions / 4, R1 → R2 | Operator exchanges, R1 → R2 | Comparison disposition |
| --- | --- | --- | --- | --- |
| FIRST-mode v0 | 3 → 2 | 1 → 2 | 1 → 1 | valid pair |
| matt-codex-port-v0 | 4 → 4 | 0 → 0 | 3 → 2 | valid pair |
| pstack-codex-port-v0 | 2 → 2 preserved partial | 2 → unknown | 1 → 1 preserved | R2 excluded; no completed pair |
| Neutral | 0 → 3 | 4 → 1 | 0 → 1 | valid pair |

Round 2 completed S02 records contain zero FACT_LOOKUP questions. Reversible engineering question items were FIRST 4, Matt 3 and Neutral 2. These count recorded classified items; grouped product questions count toward surfaced/4 by unique frozen semantics, rather than exchange count. Engineering questions received no extra product preference. Decision exchanges and implementation choices are archived.

N-S02-002 asked about existing Runs, scheduled starts and manual Runs. Only those three semantics were answered. Resume catch-up behavior was not volunteered; the correct unasked behavior remains one silent assumption. P-S02-002’s two preserved asked/answered decisions are partial process evidence, not a final discovery or acceptance result; no remaining silent-assumption total can be assigned to its lost candidate.

**Replicated signal.** Matt’s frozen port surfaced all four product decisions with zero silent assumptions in both rounds. FIRST surfaced some decisions but left at least one silently assumed in both rounds. These are narrow repeated observations on this task and port.

**Non-replicated signal.** FIRST’s exact coverage changed from 3/4 to 2/4. Neutral’s absence of elicitation in Round 1 did not recur: Round 2 surfaced 3/4. The observed discovery gap between Matt and Neutral narrowed from four decisions to one. Pstack’s discovery stability cannot be concluded from an excluded partial run.

Correct acceptance therefore does not establish complete elicitation, and the two rounds do not show that Neutral invariably guesses or that any method guarantees requirement discovery.

Evidence: [S02 metrics](./cross-round-metrics.json), [F-S02-002](./results/F-S02-002/run.json), [M-S02-002](./results/M-S02-002/run.json), [N-S02-002 exchange](./results/N-S02-002/operator-exchange-01.json), [P-S02-002 preserved exchange](./results/P-S02-002/operator-interactions-live.json).

## S04: debugging stability

**Observation.** FIRST, Matt and Neutral have valid S04 pairs. In each pair both rounds preserved a valid failing public regression before the fix, identified premature retry-branch failure-alert emission, removed that one production call, reverified the symptom/regressions and passed the frozen evaluator. Distinct failed Runs and retry recovery remained accepted.

| Treatment | Round 1 | Round 2 | Replication assessment |
| --- | --- | --- | --- |
| FIRST-mode v0 | PASS; red → fix → green | PASS; red → fix → green | repeated mechanism and acceptance |
| matt-codex-port-v0 | PASS; red → fix → green | PASS; red → fix → green | repeated mechanism and acceptance |
| pstack-codex-port-v0 | CONTAMINATED; hidden evaluation skipped | PASS; red → fix → green | valid R2 observation; no valid matched replication |
| Neutral | PASS; red → fix → green | PASS; red → fix → green | repeated mechanism and acceptance |

All four valid Round 2 runs applied the same one-line production deletion; their public regression coverage and evidence footprints differed. FIRST/Matt/Neutral used 0/2/0 helpers in both rounds; pstack used two in valid Round 2. P-S04-001’s partial code/check claims remain excluded.

**Replicated signal.** Deterministic feedback and correct terminal-Run alert ownership recur across all three eligible pairs, including Neutral. This shows reproducibility of the fixture solution; it does not isolate a unique methodology advantage.

**Non-replicated or unmeasured signal.** A debugging speed, action-count, speculative-fix-rate or root-cause-discovery advantage is not established. Exact steps to the first valid red signal are not comparable from partial traces. Matt’s early Round 2 harness invocation/status errors were retained and are not counted as valid defect reproductions; later correct-surface red evidence supports the run. No leftover diagnostic instrumentation is present in the production candidates. Exhaustive counts of wrong-file edits/rejected fixes are unavailable.

The unchanged evaluator exports aggregate acceptance/failures, not passed/total case counts. Concurrency, crash recovery and cleanup of existing historical alerts were outside the demonstrated sequential Python/SQLite/WSGI scope.

Evidence: [S04 metrics](./cross-round-metrics.json), [F-S04-002](./results/F-S04-002/run.json), [M-S04-002](./results/M-S04-002/run.json), [P-S04-002](./results/P-S04-002/run.json), [N-S04-002](./results/N-S04-002/run.json).

## Contamination, host failure and other incidents

- **P-S04-001, Round 1: CONTAMINATED / excluded / no retry.** An unscoped `collaboration.list_agents` call returned peer result summaries and commit references. The contestant stopped; evidence was preserved; hidden evaluation was skipped. P-S04-002 is the independently scheduled Round 2 run, not a replacement.
- **P-S02-002, Round 2: INVALID_HOST_FAILURE / excluded / no retry.** On resume, previous lead/helper contexts, working area and local history were unavailable. There was no recoverable final candidate tree, candidate branch or independently verifiable public/hidden outcome. One exchange and two visible checkpoints survive. The prepared start and original evidence remain unchanged; a claimed short implementation hash is not accepted as a recoverable candidate. The batch continued at P-S01-002.
- **M-S02-001, Round 1: recorded discovery interruption; not established contamination.** Same-arm assigned-source filenames were discovered and self-flagged. The preserved administrative allowlist ruling established no forbidden-information receipt; the same incomplete reviewer resumed without replacing the run.
- **M-S04-002, Round 2: recorded write-scope deviation; not established contamination.** Validation wrote a formatted copy of its own report to an external temporary path. No outside/peer/evaluator content was received. The action and ruling were preserved; the orchestrator archived/hashed the own-report copy and removed it before the next delivery. The same candidate remained; no retry occurred.
- **F-S01-002, Round 2: recorded host provenance.** A generic cloud runtime skill was read under a higher-priority host instruction. The durable disclosure establishes no peer/hidden or alternate benchmark-method receipt; FIRST’s assigned method remained unchanged.
- No contamination or host failure was observed in the four resumed runs. Available declarations and records support that statement; they are not an exhaustive access audit.

See [profiles](./profiles.json), [P-S02-002 disposition](./results/P-S02-002/run.json), [M-S04-002 incident](./results/M-S04-002/write-scope-incident.json), [F-S01-002 provenance](./results/F-S01-002/host-provenance.json), and unchanged Round 1 records.

## Interpretation and next experiment

**Observations:** acceptance, asked/answered semantics, recorded helper structure, final production/test diffs and artifact footprints above are inspectable. Both rounds have one excluded run, for different reasons.

**Replicated signals:** acceptance on ten valid matched pairs; minimal S01 application changes and the method-arm helper structures; complete Matt S02 elicitation and partial FIRST elicitation; correct S04 terminal-Run ownership and valid red/green feedback in three eligible pairs. “Replicated” here means observed in both single-shot rounds, not statistically established stability.

**Hypotheses:** explicit frontier recomputation may help surface all S02 decisions; required fresh reviews may explain part of the S01 evidence footprint; task-sensitive mechanical exceptions may reduce pstack packaging overhead. These mechanisms were not isolated by ablations, and evidence packaging, host behavior and individual sampling are alternative explanations.

**Unsupported conclusions:** a universal winner, a native Cursor-versus-Codex comparison, causal speed/cost superiority, guaranteed completeness or safety, statistically significant effect sizes, or stable failure/contamination rates. No subjective learning/maintainability score was assigned by a treatment-aware orchestrator. A single run per cell per round, two missing valid pairs, original Neutral S01 trace gaps, procedural isolation, unverified identity and missing usage/raw traces limit inference. Reversing order does not independently estimate an order effect.

A future cohort should be declared before outcomes, retain this cohort and its exclusions, repeat multiple runs per cell with stronger trace/identity capture, and isolate candidate mechanisms while preserving independent evaluation. Production integration requires a separate evidence-backed proposal; this report makes no production change.

## Durable outputs

- [Round 2 profiles, including the excluded partial run](./profiles.json)
- [Cross-round machine-readable metrics and footprint definitions](./cross-round-metrics.json)
- [Round 1 enriched comparison view; original files unchanged](./evidence/round1-comparison-view.json)
- [Final audit](./final-audit.json)
- [Completed batch](./batch.json) and [resume state](./resume-status.json)
- [Resume host-binding/evidence-only adapter notes](./evidence/resume-host-binding.json)

All research stays on `research/batch-orchestration-round2`. Nothing was merged to main.
