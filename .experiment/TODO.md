### Feature

**You own the design. Plan, review, verify.** Delegate implementation. Stay in the lead.

1. `how` over the affected subsystem.
2. `architect` for parallel design exploration.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the **separate-before-serializing-shared-state** principle skill). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Delegate code-writing to a subagent using your configured feature model (default `grok-4.7-xhigh-fast`) with a specific scope (file paths, named data shape and its organizing structure per **principle-model-the-domain**, a state machine over scattered booleans, a table/registry over branching, a typed model over repeated shape assumptions, chosen before the delegate writes logic, and success criteria). When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate via the **arena** skill instead so the runners surface the alternatives and the cross-judge guards the pick. Mandatory: no skip-with-reason escape, and Laziness Protocol does not override it (the gain is review separation, not lines saved). A subagent forbidden to spawn satisfies this by owning the diff directly with the same review separation. No "standing by" reply that waits on a nested agent. Comments per **Comments**. Surgical edits, re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Rebase into small, ordered commits. Stack follow-ups.
   Use the **sequence-verifiable-units** principle skill, building, verifying, and committing each small unit before the next.
7. If the design is contested, `interrogate` before shipping.
8. Run **Opening a PR**.

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline. That owner fans out internally after the blocking phase. Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries. Spawn a fresh owner rather than chaining interrupts.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.

## Port dispositions

1. Completed by direct lead trace. The literal heading is in RelayBoardApp.render_dashboard and GET /dashboard returns it through the WSGI HTML response. Skip How helper because the method permits direct tracing for simple scope.
2. skip: A text-only one-file edit crosses no function boundary and has no architectural choice.
3. Blocking first steps. Locate the rendered heading and capture the existing public response before editing.
   Independent workstreams. n/a: One literal change, checks and review run serially.
   Shared mutable state. n/a: Only the lead writes production code. Reviewer reads the same checkout serially.
   Smallest safe decomposition. One lead owns the single replacement and checks, then a fresh helper reviews the diff and evidence.
4. skip: METHOD.md explicitly permits direct ownership of a truly mechanical one-file edit with separate fresh review. The data shape is an existing HTML table heading string. Retain that shape without adding state or abstraction.
5. Completed. GET /dashboard matches the exact requested replacement and GET /api/jobs matches its baseline. Full public suite passes 5 tests. Captured logs and fresh helper reruns agree.
6. Verification and fresh review completed. Candidate and evidence commits are recorded in REPORT.json and the final handoff. Rebase is unnecessary because the isolated run begins at the supplied initial commit and has no upstream changes.
7. skip: The requested wording is explicit and no design is contested.
8. Native Opening a PR is unbundled. METHOD.md substitutes handing a local immutable commit to the orchestrator. No external publication in the contestant context.

Unsupported native routes. unslop, technical-writing, create-skill, deslop, no-comments, control-ui/control-cli and Opening a PR are not bundled or installed. Apply the frozen port bindings with scoped diff cleanup/review, direct public WSGI checks and local commit handoff. Show me your work template, helper script and native transcript directory are unbundled. Use the documented TSV header and captured public commands, not invented transcripts. No native model diversity or parallel throughput claim.

Principles used. Laziness Protocol selects the single literal replacement. Model the Domain retains the existing HTML string and adds no abstraction. Prove It Works selects the real WSGI dashboard response. Test Behavior, Not Implementation selects public requests and literal user-visible expectations. Sequence Work into Verifiable Units selects baseline, one edit, verification, review, commit. Never Block on the Human uses standing authorization for reversible local work. Fix Root Causes was read but is not applied because this is an explicit wording change rather than a reported defect.
