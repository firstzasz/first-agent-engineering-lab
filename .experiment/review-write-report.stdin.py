from pathlib import Path
from datetime import datetime, timezone
report = '''# Fresh serial review

Verdict is accept with evidence and documentation Attention flags. No production correctness blocker was found in the scoped diff from `6621c8b2f3618b35dc6f0c784acf51f44fa053e8` to `b04219d12bf6e1d60782a75e354bac273a7168bd`. No application, test or upstream file was changed by this reviewer. `.experiment/review-clean-candidate.log` records a clean scoped candidate after review.

Reviewer is `/root/contestant_p_s02_001/pause_review`. Requested model is GPT-6.1 Sol with High reasoning. Observed identity and usage metrics are unknown. This is the fresh serial same-model review defined by frozen `pstack-codex-port-v0`. It does not establish native multi-model validation or native throughput.

## Correctness assessment

The independent `Job.paused` field defaults to false, persists in SQLite, and appears in every Store Job snapshot. The pause writer changes only `paused`; enabled changes only `enabled`. All enabled/paused combinations remain valid. The service rejects scheduled admission before creating a Run and retains existing disabled precedence. Repeated pause/resume commands converge to the requested state. Source and scoped diff evidence are `.experiment/review-source-visible.log` and `.experiment/review-diff-visible.log`.

The WSGI adapter accepts exact POST `/api/jobs/{id}/pause` and `/api/jobs/{id}/resume` routes, returns the existing 200 Job envelope without requiring a request body, and uses existing KeyError 404 handling. GET jobs exposes the field. Missing ids, wrong methods, root-prefix variants, extra nesting and trailing components are covered by `tests/test_pause.py`. The final route guard is specific to the new commands and leaves existing route behavior intact. The recorded boundary red check failed once before the root guard was corrected. Evidence is `.experiment/pause-route-boundary-before.log`, `.experiment/pause-add-route-boundary-test.stdin.py`, `.experiment/pause-fix-route-boundary.stdin.py` and the scoped diff.

Manual Run creation and all Attempt/retry/alert logic are unchanged in the production diff. This matches the recorded operator response, which explicitly allowed manual Runs and preserved current Runs through terminal outcome including existing retries and alerts. The broader-than-glossary retry failure alert remains deliberately intact. Current-Run retry then success, preserved alert, manual terminal failure and enabled independence are asserted by public WSGI tests. Dashboard preserves prior columns, values and terminal-result selection while appending Paused visibility. No extra product semantics were introduced. Evidence is `.experiment/operator-interactions.jsonl`, `tests/test_pause.py`, and the scoped diff.

The additive migration adds only `paused INTEGER NOT NULL DEFAULT 0` if the jobs table lacks it. Reopening is idempotent. The public legacy test creates history after its first migration, so it is not direct evidence that history predating migration survives. I closed that verification gap using a read-only public check with all four legacy tables and preexisting Run, Attempt and Alert rows. Exact tuples were preserved; Job default, paused admission after reopening, dashboard history, alert id and resumed scheduling all passed. Source and output are `.experiment/review-preexisting-history.stdin.py` and `.experiment/review-preexisting-history.log`.

The existing read-then-create scheduler admission is not atomic across concurrent connections. Pause introduces another admission flag using that same boundary. This review establishes serial fixture behavior, not linearizable concurrent scheduling. The design explicitly records the accepted existing limitation; no concurrency redesign is warranted by the supplied scope.

## Verification and method audit

I read TASK, METHOD, grounding, design, throughput, implementation report, lead review, decisions and operator records top to bottom. I followed relevant command pointers and reviewed the complete scoped diff and application/public tests. `.experiment/review-command-map.log` maps recorded argv, exit codes and output files and found no missing command output. Initial reads and source provenance are represented by `.experiment/initial-actions.json` and `.experiment/sources.json` with their disclosed limits.

Observed checks support the reported results. Baseline output contains five passes. `.experiment/pause-focused-before.log` contains ten tests with seven failures and three errors. `.experiment/review-commit-scope.log` shows the tests-only commit `087535a1e0b0ddf43cf4e9e843f76c297d6bce66`. Initial green and final green logs report ten focused and fifteen public passes. Lead independent focused/full outputs also report ten and fifteen passes. `.experiment/lead-api-surface.stdin.py` and `.experiment/lead-api-surface.log` contain literal expected WSGI pause, blocked scheduled, allowed manual, resume and accepted scheduled responses. Final diff checks record exit zero. I did not rerun the already-passing suites because the one unresolved migration concern had a targeted check.

The grounded Job shape, structurally distinct relation alternative, synthesis and four throughput items precede implementation in recorded checkpoints. Model the Domain supports independent state on the existing Job; no synchronized flags were introduced. Laziness Protocol supports the small Store/service/adapter change without a new relation or module. Prove It Works and Test Behavior, Not Implementation shaped this review's literal WSGI and preexisting-history comparison. Sequence Work into Verifiable Units is supported by tests-only then production commits and red/green outputs. Show me your work shaped the command-pointer and provenance audit. Applicable bundled core, Feature, How, Architect, red flags, rationale and leaf sources were read locally in `.experiment/review-method-sources.log`, `.experiment/review-leaf-visible.log` and `.experiment/review-design-sources.log`. No unbundled native capability was fetched.

## Actionable scoped issues

1. Documentation only. `.experiment/TODO.md` still labels completed How, design, implementation and verification phases pending or in progress. Update it to actual completion/skip states before final handoff so it agrees with the decision log and reports.
2. Evidence provenance only. The lead's `07:09:44.569952+00:00` verification/review rows follow the implementation helper's start marker without a lead return start marker. Show me your work uses start rows to delimit authorship. Append a correction identifying those rows as lead-owned; preserve existing rows. The verification row points only at the API log for focused/full counts. Append a superseding pointer row to `.experiment/lead-focused.log`, `.experiment/lead-full-public.log` and `.experiment/lead-api-surface.log`.
3. Claim precision. Cite the reviewer preexisting-history check for preservation across the initial migration. The committed public legacy test proves migration default plus preservation across subsequent reopening, rather than history existing before migration. No code defect was exposed and no production change is requested.

## Attention

Reviewed by requested GPT-6.1 Sol High; observed identity unknown.

- Earlier inline stdin commands have argv/output records but no archived raw input. Initial direct listings/reads have reconstructed records, not dedicated command capture. Complete raw transcript is unavailable. The ordered commits, outputs and visible checkpoints support the limited claims above; they cannot establish a complete action history. Keep this limitation visible.
- Stale TODO state and lead-return provenance/pointer issues above need evidence-only corrections before handoff.
- Initial pre-migration-history coverage was narrower than a casual reading of the legacy test name suggests. The reviewer check passed and supplies direct public evidence.
- Concurrent admission remains an accepted existing limitation. No concurrency correctness, observed identity/usage metrics, multi-model or native throughput claim is made.

No deliberate hidden-material retrieval was observed in the captured command/path evidence or performed by this reviewer. This is a statement about the available capture, not proof of an unavailable full transcript. No sibling/control paths, external resources, remote git, deployment, credentials or descendants were accessed by this reviewer.
'''
Path('.experiment/helper-review-report.md').write_text(report)
rows = [
    ('start','Fresh serial reviewer audits candidate and captured evidence','METHOD requires separate code and trail review','.experiment/helper-review-report.md','Prior rows from 2026-10-07T00:00:00Z through 2026-10-07T07:09:44.569952+00:00 were not authored by this reviewer'),
    ('review','Accept pause candidate with evidence-only Attention flags','Scoped source and public outcomes reveal no correctness blocker','.experiment/helper-review-report.md','Update TODO and lead return provenance; preserve capture limitations'),
    ('verify','Check history that genuinely predates additive migration','Committed legacy test creates history after first migration','.experiment/review-preexisting-history.stdin.py; .experiment/review-preexisting-history.log','Pass; preexisting Run Attempt Alert tuples preserved with pause reopen resume behavior')
]
with Path('.experiment/decisions.tsv').open('a') as handle:
    for row in rows:
        handle.write(datetime.now(timezone.utc).isoformat()+'\t'+'\t'.join(row)+'\n')
print('Wrote helper-review-report.md and appended three reviewer decision rows. No code or test edits.')
