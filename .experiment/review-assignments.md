# Review assignments

## Standards

- Helper task: /root/contestant_m_s01_001/standards_review.
- Requested model: gpt-6.1-sol; reasoning: high; fork_turns: none.
- Read-only root: /workspace/relayboard-active/M-S01-001; explicit workdir required; no descendants.
- Diff: git diff 5e8146a112483d7ef33d493c0f1f1dae0ffba8cb...HEAD; candidate 7e60748606eace908629ebfd6504de7f2246de77; commit 7e60748 Change Jobs dashboard heading to Latest result.
- Allowed sources: TASK.md, METHOD.md, public relevant code, README.md, pyproject.toml, assigned upstream/matt/skills/engineering/code-review/SKILL.md. No other review reports.
- Restrictions delivered: no siblings/control directories, lab history/branches/results, evaluator/oracle/reference solutions, private transcripts/credentials, unassigned methods, peer statuses, team-wide enumeration, hidden checks, fetches, paid API, external messages, production, deployment or merges. Stop/report/preserve on forbidden exposure.
- Brief: Standards only; cite documented standard violations and separately label heuristic smells per file/hunk, quoting relevant hunk, under 400 words. No documented standards source found by lead; actual existing style and baseline still apply. Skip tooling-enforced checks. Return command/output and path evidence, requested vs observed identity, limitations, then terminate.
- Initial spawn included the complete set of baseline smells in compact wording. A follow-up supplied the verbatim baseline descriptions and fixes from the assigned source, with repo-override and judgment-call rules, replacing the compact wording. This administrative correction did not supply any review findings.
- No product questions or operator exchange involved.

## Spec

- Helper task: /root/contestant_m_s01_001/spec_review. Spawned only after receiving Standards helper's final answer/termination.
- Requested model: gpt-6.1-sol; reasoning: high; fork_turns: none.
- Same read-only root, explicit workdir, no descendants, and complete experiment-boundary restrictions as Standards. Forbidden exposure requires stop/report/preserve.
- Diff and candidate commit identical to Standards; TASK.md is the supplied spec.
- Allowed inputs: TASK.md, METHOD.md, .experiment/decisions.md, relevant public code, assigned code-review source, and lead's heading-red/heading-green/completion-public/scope-check evidence. No Standards review-output access.
- Brief: Spec only; report missing/partial requirements, unrequested scope creep, or incorrectly implemented requirements; quote originating spec for each finding; findings under 400 words. Return commands/relevant outputs, path access, identity observations, limitations; then terminate.
- Exact task supplied: change Jobs dashboard heading from Last result to Latest result; no API or unrelated dashboard changes; implement and verify. Tiny TASK.md unit, no separate spec/tickets/questions; existing public WSGI seam standing-authorized.
