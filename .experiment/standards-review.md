# Standards review — fresh read-only helper

Hard breaches: none found. Changes preserve README.md’s standard-library Python/SQLite/WSGI approach and small, inspectable system. No additional documented coding standards were supplied; tooling-enforced issues excluded.

Heuristic smells:

- Possible Duplicated Code — relayboard/web.py, added pause/resume handlers. Both repeat `job_id = path.split("/")[3]` and `{"job": self._job_json(self.store.get_job(job_id))}`, with identical method/prefix checks, response status and serialization. A small shared action dispatch or response helper could keep these handlers consistent. Low severity; existing routing uses similar explicit branches.
- Possible Duplicated Code — relayboard/store.py, get_job/list_jobs hunks. Both now repeat the same row-to-Job mapping, including `bool(row["paused"])` and `bool(r["paused"])`. A single row conversion helper would prevent future Job-field additions from requiring synchronized constructor edits. Low severity; duplication predates this change, which expands it.

No actionable findings from remaining smell baseline. No product/spec assessment performed.

Factual evidence: All shell calls explicit assigned workdir. Commands:

```text
pwd
rg --files -g 'METHOD.md' -g 'README.md' -g 'pyproject.toml' -g 'SKILL.md' -g '*review*'
cat METHOD.md
cat upstream/matt/skills/engineering/code-review/SKILL.md
cat README.md
cat pyproject.toml
git diff 1c8287bdf072be0b0a4248cded22951b95568928...HEAD
git diff 1c8287bdf072be0b0a4248cded22951b95568928...HEAD -- relayboard tests GLOSSARY.md
sed -n '1,130p' relayboard/store.py
sed -n '1,160p' relayboard/service.py
sed -n '1,150p' relayboard/web.py
cat tests/test_public.py
cat relayboard/models.py
cat relayboard/testing.py
```

Unrestricted assigned-run diff displayed portions of .experiment/* and .scratch/work/spec.md; not used for product assessment. Truncated output; relevant code/test hunks reread with scoped diff. No tests, mutations, network, descendants, other-run access or external messages. Starting-point resolution/commit identity supplied by lead, not independently verified. Requested GPT-6.1 Sol/high; observed identity/usage unknown. Helper contamination flag: none observed.
