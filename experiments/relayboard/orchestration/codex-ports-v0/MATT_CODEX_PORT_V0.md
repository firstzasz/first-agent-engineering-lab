# matt-codex-port-v0

Status: FROZEN BEFORE NEW BENCHMARK OUTCOMES
Upstream: mattpocock/skills, 4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d.
License: MIT, Matt Pocock. Exact consulted source files are bundled unchanged under upstream/matt/.
Version changes require a new label and comparison cohort.

## Defined adaptation

Explicitly invoke the applicable bundled Matt skills by opening their files. Codex has no native Claude Skill tool/plugin or configured external tracker. Local files are the configured tracker. Slash invocation means read and perform the named workflow with this fixed host binding.

Local spec path is .scratch/work/spec.md; tickets are one file each under .scratch/work/issues/, with numbered blockers and statuses. Use TASK.md as originating spec for a tiny task that needs no additional spec. Reversible ticket-shape approvals are standing under the user's autonomous instruction; product decisions still wait for requested operator answers. Existing public fixture interfaces are the pre-agreed test seams for this port; if an interface change itself raises a product decision, ask the operator. This deliberately removes native setup/approval round trips and must be counted as an adaptation.

Native parallel subagents and integration worktrees become sequential fresh Codex helpers within the run's local integration branch. Native model diversity is absent. Freshness and separate review axes remain; parallel throughput is not claimed. Fresh helpers use the normalized model and may not spawn descendants.

## Invocation and routing

1. Read TASK.md, GLOSSARY.md and relevant public code/tests before choosing a route. Read only this arm's bundled methodology.
2. For an underspecified feature invoke grill-with-docs, which composes bundled productivity/grilling and engineering/domain-modeling. Map decisions as a dependency tree. Ask each currently answerable frontier of genuine product/preference questions, wait for operator answers, then recompute. Empirical facts come from the workspace. Record resolved terminology inline when useful; create ADRs only for a genuine durable tradeoff. Do not use hidden answer sheets or benchmark acceptance hints.
3. Once decisions are established, invoke to-spec: synthesize known context without re-interviewing. Prefer existing highest public seams and capture problem, solution, user stories, implementation/testing decisions, scope and notes. For a feature requiring multiple units, invoke to-tickets to write verifiable vertical slices with actual blocking edges; never use a horizontal layer checklist as the task graph. A narrow mechanical change can use TASK.md with one implementation unit; record why no interview/spec/ticket ceremony was useful.
4. Invoke implement for one unit, or implement-spec for the graph. The local candidate branch is the integration branch. Work the ready frontier serially. For a ticket graph, fresh bounded implementer helpers can implement one ticket at a time in the dedicated area, followed by the lead's integration verification; shared writes never overlap. The lead may implement a single small unit directly.
5. Apply bundled TDD rules to features: observable public seams, literal independent expectations, red before green, one test and minimal implementation per vertical slice. Do not bulk-write imagined tests. Prefer real test SQLite/WSGI interfaces rather than mocking internal collaborators. Refactoring belongs to review, not speculative red/green expansion. No language-specific typechecker is invented for this standard-library Python fixture.
6. For reported bugs invoke diagnosing-bugs before theory-driven code changes. Build a tight deterministic red-capable command for the actual reported symptom, reproduce and minimize, then write 3–5 ranked falsifiable hypotheses before testing them. Send the hypothesis checkpoint without blocking. Instrument one predicted boundary at a time, establish the cause, write a regression check before the fix at a valid public seam, rerun the original repro and clean instrumentation. Justify skipped phases and document any unavailable seam.
7. Run focused checks during implementation and the full public suite at completion. Commit locally in verifiable units.
8. Invoke code-review on a fixed local starting commit. Keep Standards and Spec axes separate. Run two fresh same-model Codex review helpers sequentially, each read-only within this run: one compares the diff to actual standards and the upstream smell baseline; the other compares it to TASK.md plus this run's resolved spec/decisions. Aggregate without collapsing axes. Fix legitimate public-review issues before freezing. No hidden evaluation occurs here.
9. Finish with the candidate commit/diff, spec/ticket status where used, question/answer and decision record, exact public verification outputs, review findings per axis and declared limitations. Orchestrator publication replaces native tracker PR/issue closure. Do not change or close external parent issues.

## Declared semantic losses

Native plugin discovery/Skill invocation, external tracker semantics, parallel ready-frontier throughput, worktree merging roles and interactive seam/ticket approval are replaced as described. Two-axis fresh-context review and source TDD/diagnosis rules are retained. This arm is the frozen Codex port, not a native Matt-host or unchanged upstream execution.

## Binding precedence and experiment boundary

This is a frozen, explicitly non-native Codex port. The pilot protocol and task scope override upstream shipping/deploy/external-message instructions. Work only in the assigned contestant area. No other run, evaluator/oracle/reference-solution, lab history or result inspection. The repository is public; deliberate hidden-material retrieval is contamination, not a reason to pretend hard secrecy. Stop and report any such access; preserve evidence.

Use GPT-6.1 Sol with High reasoning for the lead and any helpers where supported. Record requested versus observed identity. Every helper uses fork_turns=none, receives only this run's task/method/files, and works only under this run's root. Execute helpers sequentially and wait for each to finish before another. No helper may fetch the lab repository. No native plugin, native model diversity or throughput claim is made.

Questions go to the benchmark operator through collaboration.send_message(target="/root", message="OPERATOR QUESTION ..."), not to a human UI. Ask genuine product/preferences only when the method calls for them; do not receive product answers before asking. Administrative authorizations for reversible local work are standing. If the method seeks approval of a reversible test seam or ticket shape, use existing public fixture interfaces and record the standing authorization; do not treat it as product guidance.

All work is local Python/SQLite/WSGI and git. No paid API, credentials, production system, production repository, deployment, shipping or merging to main. The orchestrator, after termination, publishes candidate commits/PRs to the assigned treatment branch and separately evaluates the frozen candidate. Hidden evaluation is never part of the contestant workflow. No hidden-feedback retries.

Preserve source version, routes/skills invoked, adaptations, local commits, decisions, tests and available evidence. Claims require their actual command/output or an explicit unknown label.
