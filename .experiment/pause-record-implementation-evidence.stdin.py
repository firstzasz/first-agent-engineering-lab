from pathlib import Path
from datetime import datetime, timezone
rows = [
    ['implementation', 'Persist independent paused bit and guard scheduled admission', 'Model the Domain places pause on Job; Laziness Protocol uses existing Store/service boundaries', '.experiment/pause-final-scoped-diff.log', 'Manual Runs, record_attempt and alert emission unchanged'],
    ['review', 'Require exact root prefix for pause/resume routes', 'Self-review found a prefix without leading slash was accepted; reproduce before correcting guard', '.experiment/pause-route-boundary-before.log', 'One expected failure then ten focused tests pass'],
    ['verify', 'Complete focused and full public checks on final code', 'Prove It Works observes WSGI responses, SQLite persistence and preserved behavior', '.experiment/pause-focused-final.log; .experiment/pause-full-public-final.log; .experiment/pause-final-diff-check.log', '10 focused and 15 full tests pass; git diff --check exits 0'],
    ['audit', 'Label early command-input capture limitations', 'Do not claim a complete raw transcript; initial listing bypassed wrapper and old wrapper omitted stdin script source', '.experiment/helper-implementation-report.md', 'Output and argv captured for checks; old inline input unknown from command artifacts'],
]
with Path('.experiment/decisions.tsv').open('a') as log:
    for row in rows:
        log.write('\t'.join([datetime.now(timezone.utc).isoformat(), *row]) + '\n')
with Path('.experiment/helper-implementation-report.md').open('a') as report:
    report.write('''
## Implemented behavior

Job now has `paused: bool = False`. Store initializes `paused INTEGER NOT NULL DEFAULT 0`, adds that column when a legacy jobs schema lacks it, reads it into Job snapshots and owns the single `set_job_paused` writer. Service pause_job/resume_job return Job and converge idempotently. Scheduled admission checks paused before creating any Run. Existing disabled rejection retains precedence for disabled and paused Jobs.

The WSGI adapter accepts exact POST `/api/jobs/{id}/pause` and `/api/jobs/{id}/resume` routes without requiring a body and returns 200 with the existing Job envelope. Unknown Job ids use the existing 404 envelope. Scheduling while paused uses the existing 409 handling. GET jobs includes paused. Dashboard appends Paused after the existing Job, Enabled and Last result columns.

No changes were made to manual admission, record_attempt, Run/Attempt/Alert shapes, retry or alert emission. Existing public tests and bundled upstream sources remain intact. A retry failure currently emits an alert; the new current-Run test deliberately preserves that observed behavior and its alert after later success.

## Ordered local commits

Tests first commit `087535a1e0b0ddf43cf4e9e843f76c297d6bce66` contains the ten initial behavior tests and no production edits. Implementation commit identity will be appended after commit.

## Verification

All checks below ran through `.experiment/run_command.py` with cwd confined to this run.

| Exact command | Captured output | Result |
| --- | --- | --- |
| `python .experiment/run_command.py pause-focused-before -- python -m unittest discover -s tests -p test_pause.py -v` | `.experiment/pause-focused-before.log` | Exit 1, 7 failures and 3 errors on unchanged production baseline. |
| `python .experiment/run_command.py pause-focused-after -- python -m unittest discover -s tests -p test_pause.py -v` | `.experiment/pause-focused-after.log` | Exit 0, initial 10 tests pass. |
| `python .experiment/run_command.py pause-full-public-suite -- python -m unittest discover -s tests -v` | `.experiment/pause-full-public-suite.log` | Exit 0, initial 15 tests pass. |
| `python .experiment/run_command.py pause-route-boundary-before -- python -m unittest discover -s tests -p test_pause.py -v` | `.experiment/pause-route-boundary-before.log` | Exit 1, one strengthened exact-route assertion fails because prefix/api/jobs/daily-report/pause returned 200. |
| `python .experiment/run_command.py pause-focused-final -- python -m unittest discover -s tests -p test_pause.py -v` | `.experiment/pause-focused-final.log` | Exit 0, final 10 tests pass after requiring exact root prefix. |
| `python .experiment/run_command.py pause-full-public-final -- python -m unittest discover -s tests -v` | `.experiment/pause-full-public-final.log` | Exit 0, final 15 tests pass. |
| `python .experiment/run_command.py pause-final-diff-check -- git diff --check` | `.experiment/pause-final-diff-check.log` | Exit 0, no whitespace errors. |
| `python .experiment/run_command.py pause-final-scoped-diff -- git diff -- relayboard/models.py relayboard/store.py relayboard/service.py relayboard/web.py tests/test_pause.py` | `.experiment/pause-final-scoped-diff.log` | Self-reviewed final scoped diff. |

The ten tests cover default unpaused state, repeated pause/resume, rejected scheduling without creating a Run, allowed manual Runs, enabled/paused independence, resume while disabled, unknown ids, exact routes, current retry/success and preserved alert, paused manual terminal failure, dashboard existing values and pause visibility, file database reopening, and a legacy jobs schema migration followed by Store reopening with preserved history.

## Throughput and open decisions

Blocking grounding/design work was supplied by the lead and read before production edits. This helper owned tests and the cohesive four-file implementation serially. Store remained the only pause writer. The smallest safe decomposition remains implementation helper, lead independent verification, fresh serial review. No native parallel throughput or multi-model review is claimed. No product decisions remain open in this scope.

## Evidence capture limitations

The first read-only tool command ran `pwd && rg --files ...` directly in the assigned root before using the required wrapper. It was a method capture deviation, not hidden-material retrieval. All subsequent checks used the wrapper. That listing output exists in the tool conversation but has no dedicated `.experiment` command record.

Earlier inline-input commands `pause-record-assignment`, `pause-write-behavior-tests`, `pause-record-red-tests`, and `pause-implement-feature` were executed by the old wrapper. It saved argv and output but did not archive Python stdin source. The resulting tests and code are reviewable in ordered commits and captured diffs; the raw input is not recoverable from those command artifacts and is not claimed. The lead updated the wrapper before `pause-add-route-boundary-test`, so later inline source is archived as `.stdin.py` beside its log. File-read commands used `python -c` and retained their script in argv.

## Attention

Independent review is pending with the lead. Observed model identity is unknown. No hidden material was deliberately retrieved, no descendants spawned and no external material fetched. Existing concurrent scheduling admission and retry-alert behavior are outside scope. The capture limitations above should remain visible in the final trail.
''')
