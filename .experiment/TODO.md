# Bug fix playbook

### Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix to subagents, stay in the lead.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself on the matching surface via the control skill (Non-negotiables), even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with `how` over the affected subsystem and the **why** skill for regression history. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt with Cursor's `/loop` command. Confirm the surviving *mechanism* with runtime evidence before the step-3 architect/interrogate fan-out.
3. Plan the fix. If it crosses a function boundary, `architect` first. Delegate implementation to a subagent using your configured bug-fix model (default `grok-4.7-xhigh-fast`) with a specific scope.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history. See the **tdd** skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical **sequence-verifiable-units** principle skill, the failing test first and the fix on top.
6. Run **Opening a PR**.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.

# Task-specific checkpoints

- Read assigned sources and trace the public API to the attempt transition. Done.
- Reproduce duplicate failure alerts before changing production code. Done.
- Add and commit failing public regression tests. Done.
- Compare two written designs after confirming the mechanism. Done.
- Delegate bounded implementation to a fresh serial helper. Done.
- Verify public API, focused tests, and complete public suite. Done.
- Review scoped diff and obtain fresh serial code/evidence review. Done.
- Freeze local candidate commit and report. Production committed; evidence-only commit containing this checklist completes the freeze.

# Native step dispositions

- Step 1 control plugin. Adapted to existing WSGI request surface.
- Step 2 why regression history. Unsupported and unbundled. No lab history inspection. Runtime evidence and current assigned source ground the diagnosis.
- Step 2 loop. Adapted to serial evidence/change/verify loop.
- Step 3 architect. Two serial lead-written sketches, as specified by METHOD.md.
- Step 6 Opening a PR. Skip native opening/deploy/merge. Commit locally for orchestrator publication under METHOD.md.
