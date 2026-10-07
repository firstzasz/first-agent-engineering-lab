# EXP-0009: Neutral S01 pilot run

Status: VERIFIED (behavior), observational metrics incomplete

Date: 2026-10-07

## Research question

Can a fresh neutral coding agent complete the small S01 dashboard-label change correctly, without altering unrelated behavior, when started from an evaluator-blind frozen workspace?

This pilot validates the end-to-end treatment and examiner process. It does not compare the four methodologies.

## Setup

- Scenario: `S01-v0`
- Treatment: `neutral-v0`
- Base fixture: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`
- Prepared workspace commit: `563952fab378eda87da696cda4df12fe5c9d4e5e`
- Host/model (operator-reported, not machine-attested): OpenAI Codex Cloud, OpenAI 6.1 Sol, High reasoning
- Agent output: [PR #15](https://github.com/firstzasz/first-agent-engineering-lab/pull/15), exact candidate head `d1685e9697054e7c78b9c9a0317809021adabc90`

The evaluator was not available in the agent's prepared workspace. This research conversation, which knows the oracle, served only as examiner and did not implement the change.

## Implementation observed

The candidate changes exactly one line in `relayboard/web.py`: the dashboard Jobs-table heading becomes `Latest result`. No other file or API contract was changed in the PR diff.

The agent reported that five public tests and a dashboard smoke check passed. Its full tool log, token count, and detailed interaction trace were not available to the examiner.

## Independent verification

The examiner created [PR #16](https://github.com/firstzasz/first-agent-engineering-lab/pull/16) containing a one-off grader that:

1. fetches the agent branch;
2. checks that its head exactly equals the pinned candidate commit;
3. checks that the file-level diff is confined to `relayboard/web.py`;
4. exports the exact candidate snapshot into an isolated workspace;
5. runs public tests and the previously frozen S01 evaluator;
6. checks the run manifest is `N-S01-001 / S01-v0 / neutral-v0`.

[GitHub Actions run 37559041286](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/37559041286) completed successfully:

- public tests: PASS;
- evaluator oracle: PASS;
- evaluator failures: `[]`;
- expected run identity: PASS;
- candidate commit pin: PASS;
- changed-file restriction: PASS.

The complete evaluation output is available as [artifact 11455762981](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/37559041286/artifacts/11455762981).

This verifies the WSGI-served dashboard markup through the fixture's request path, not rendering in a full browser.

## Observed metrics

| Metric | Observation |
| --- | --- |
| Correctness | PASS |
| Independent oracle | PASS |
| Diff | 1 file, 1 insertion, 1 deletion |
| Unrelated API contract | No changes in PR diff; public tests PASS |
| Operator questions | Unknown: full transcript not captured |
| Tool count / tokens | Unknown: host trace unavailable |
| Elapsed agent time | Unknown: no trustworthy start/end stamps |
| Learning-value rubric | Not graded for this neutral pilot |
| Contamination | No oracle in prepared workspace; wider agent browsing unverified |

## Limitations

- Only one agent run was observed.
- S01 is deliberately simple and susceptible to ceiling effects.
- The agent's model and reasoning settings were reported by the operator, not verified by the evaluator.
- The preparer workspace prevents accidental oracle exposure but cannot prove an unrestricted agent did not access public oracle data elsewhere.
- This independent run verifies behavior, not every process or operator-burden metric.
- [PR #15](https://github.com/firstzasz/first-agent-engineering-lab/pull/15) remains intentionally unmerged.

## Result

**VERIFIED PASS for the narrow S01 behavior contract.**

No claim of methodology superiority is supported.

## Next steps

- Persist this pilot result and keep PR #15 unmerged as requested.
- Run S02 and S04 neutral arms in fresh isolated contexts.
- Then compare pstack, Matt Pocock, and FIRST-mode on matched tasks/models.
- Improve capture of the agent's question count, tool count, timing, and learning-value evidence before drawing operator-fit conclusions.
