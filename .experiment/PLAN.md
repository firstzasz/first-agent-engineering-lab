# Bug fix route

Task classification is Bug fix. Done means each terminally failed Run emits exactly one failure alert, retries preserve Run identity and policy, and distinct failed Runs retain their separate alerts. Recovered Runs emit no failure alerts per GLOSSARY.md.

## Playbook steps

1. Reproduce it yourself on the matching surface via the control skill (Non-negotiables), even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with `how` over the affected subsystem and the **why** skill for regression history. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt with Cursor's `/loop` command. Confirm the surviving *mechanism* with runtime evidence before the step-3 architect/interrogate fan-out.
3. Plan the fix. If it crosses a function boundary, `architect` first. Delegate implementation to a subagent using your configured bug-fix model (default `grok-4.7-xhigh-fast`) with a specific scope.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history. See the **tdd** skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical **sequence-verifiable-units** principle skill, the failing test first and the fix on top.
6. Run **Opening a PR**.

Step 6 is adapted to a local commit and orchestrator handoff by METHOD.md. No PR or remote operation occurs in this run.

## Throughput checkpoint before implementation

- Blocking first steps. Read task, frozen method and applicable sources; reproduce via WSGI; confirm the lifecycle mechanism before delegation.
- Independent workstreams. Diagnosis, regression coverage, and evidence review are conceptually separate. Helpers execute strictly serially under METHOD.md.
- Shared mutable state. All helpers share this checkout, git index and .experiment artifacts. Only one helper runs at a time. The lead does not edit code while a code helper runs.
- Smallest safe decomposition. Lead reproduces and selects the local fix; code helper adds failing public API regression tests, records red evidence and commits tests, then removes the premature alert call; lead verifies and reviews; fresh review helper audits diff and trail; lead freezes a local candidate.

## Data shape and direct How trace

A Job owns max_attempts. A stable Run owns ordered Attempts and one terminal outcome. Alerts reference Run identity, not attempt identity. WSGI routes call RelayBoardService.record_attempt; the service records an Attempt, decides retry or terminal outcome, and writes alerts through Store. Store simply inserts the provided alert. No additional alert path exists in the supplied web surface.

How uses the simple direct lead explainer route explicitly permitted by METHOD.md. Native How references are unbundled. The scope is one lifecycle branch in one service function.

## Native routes unavailable

The bundled sources do not supply why, unslop, technical-writing, create-skill, deslop, no-comments, control-ui/control-cli or Opening a PR. These routes are not fetched or invented. METHOD.md maps control surfaces to direct WSGI checks, cleanup to a scoped diff review, and PR opening to local immutable commit handoff. Prose follows core bundled writing rules. No lab history is inspected. Native /loop becomes evidence/change/verify inside this turn. No native multi-model or parallel-throughput claim is made.

## Scope choice

The candidate fix is one deletion within record_attempt, leaving its existing terminal failure alert as the sole emission. It changes no function interface or boundary. Architect is skipped because this fix does not cross a function boundary or require cross-function design. No schema deduplication or additional abstraction is justified by the observed sequential fixture behavior. The real invariant is terminal Run failure, not one alert per Job.
