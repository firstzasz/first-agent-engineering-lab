# F-S04-002 FIRST-mode v0 work record

Boundary: only /workspace/relayboard-round2-active/F-S04-002; initial commit a48b7463d1ebad6b3e7d242654a99b4e70e7e642. No network, remote, evaluator, peer, credentials, sibling files, or history investigation.

Route: L1 legible autonomous execution. Small reversible bug with deterministic regression seam; independently inspectable executable API assertions satisfy verification without helpers. Runtime identity/usage are unknown; requested contestant identity is F-S04-002.

Goal/predicate: Retry attempts keep the same running Run and produce no failure alerts; exhausted Runs emit exactly one failure alert; successful retries emit no failure alerts; separate failed Runs of the same Job each emit their own alerts; configured attempt counts and terminal protections remain intact.

Grounding: TASK.md, frozen METHOD.md, GLOSSARY.md, README.md, pyproject.toml, relayboard service/store/models/web/testing/main/init and tests/test_public.py. README references outside the boundary were not followed.

FACT: retry branch calls _emit_failure_alert before returning retry; terminal branch calls it again. Glossary defines AlertRule after terminal outcome and distinguishes Attempts from Runs.
REVERSIBLE_ENGINEERING: remove only the premature retry-branch alert call. No schema change or Job-level suppression is needed; the existing terminal-state guard handles repeat attempt submissions.
Checkpoint: root-cause hypothesis grounded in source; reproduce with WSGI API regressions before implementing. No PRODUCT_PREFERENCE or L3 questions identified.

Initial read-only commands (outputs visible in tool transcript; exact source preserved in initial commit):
1. pwd && rg --files -g 'TASK.md' -g 'METHOD.md' -g 'AGENTS.md' -g 'package.json' -g '*lock*' -g '.experiment/**'
2. cat TASK.md METHOD.md && git status --short && git log -1 --format='%H %s' && rg --files -g '!METHOD.md' -g '!TASK.md' -g '!.git/**'
3. cat README.md GLOSSARY.md pyproject.toml relayboard/models.py relayboard/service.py relayboard/store.py relayboard/testing.py tests/test_public.py
4. cat relayboard/web.py relayboard/__main__.py relayboard/__init__.py && git status --short --untracked-files=all
All commands used explicit assigned workdir. Initial status clean and initial hash matched. These commands did not follow outside links. Subsequent executable checks are captured by record.py in commands.jsonl and output files. File-writing shell commands are recorded by the resulting artifacts and this record; no terminal-wide system audit is available.

Reproduction checkpoint: baseline 5 tests pass; new API regression suite fails with 6 failures (including 4 retry-policy/source subcases). Evidence: baseline.txt and regression-red.txt. Two interleaved Runs yielded 4 alerts instead of 2; successful retry retained a false failure alert. Source hypothesis confirmed. Removed the retry-branch alert call, leaving attempt creation, retry return, terminal transition, and terminal guard untouched.

Verification checkpoint: all 8 public and regression methods pass, including 6 exhaustion policy/source subcases; original repro is green on the WSGI API surface. git diff --check passes. Implementation commit f975c8b2bf0d4e8e36be8f710caf2821cba80daa. No helpers, operator exchanges, external access, or hidden evaluation. Remaining work: commit this evidence bundle locally, confirm clean status, report and terminate.

Final checkpoint: implementation and evidence locally committed; working tree confirmed clean after evidence commit fb3b3b109e535fde26f0009af4ddf0ec13a04126. Evidence staging whitespace check flagged verbatim unittest/diff output; preserved raw logs and explicitly recorded the result. Committed source/test diff check passes. Final report update records this distinction; no functional change or further test run needed. Status VERIFIED; no remaining authorized work after committing this final record.
