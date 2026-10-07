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


# Frozen port execution notes

# Feature route

1. `how` over the affected subsystem.
   skip: Dedicated How helper is unnecessary for one literal. Lead traced GET /dashboard through render_dashboard and the existing WSGI fixture.
2. `architect` for parallel design exploration.
   skip: No function boundary, logic, interface, or architectural choice changes.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
     Read task, frozen method, Feature playbook and applicable leaf principles. Locate the sole heading and capture the actual WSGI baseline before editing.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
     n/a: One literal in one file. No parallel workstreams.
   - **Shared mutable state.** Default to splitting the target (the **separate-before-serializing-shared-state** principle skill). Serialize only for real invariants.
     n/a: Lead owns the single source edit. Fresh reviewer is read-only and runs after verification.
   - **Smallest safe decomposition.** If one worker is best, name why.
     One lead owns the literal edit and surface check; one fresh helper reviews the diff and evidence serially.
4. Delegate code-writing to a subagent using your configured feature model.
   skip: METHOD.md step 5 explicitly permits direct ownership of a truly mechanical one-file edit with separate fresh review. No stateful logic is introduced. The data shape remains the existing HTML table and its string heading.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
   Complete. WSGI before/after check passed; all five public tests passed; fresh reviewer reran both and passed.
6. Rebase into small, ordered commits. Stack follow-ups.
   Use the **sequence-verifiable-units** principle skill, building, verifying, and committing each small unit before the next.
   One verified code unit. No remote or other branch access; commit on the existing local branch without rebase.
7. If the design is contested, `interrogate` before shipping.
   skip: Exact copy requirement, no contested design.
8. Run **Opening a PR**.
   Adaptation: Bundled PR playbook is absent. METHOD.md replaces native PR automation with immutable local commit handoff to the orchestrator.

# Routes and adaptations

Read core Poteto Mode, Feature, Laziness Protocol, Model the Domain, Prove It Works, Fix Root Causes, Test Behavior Not Implementation, Sequence Verifiable Units, Never Block on the Human, and Show Me Your Work.

Fix Root Causes is nonapplicable because this is specified copy change, not debugging. Test Behavior Not Implementation governs the WSGI check. Sequence Verifiable Units keeps this as one before/after unit. Never Block on the Human uses standing permission for the reversible edit; no product question exists.

How and Architect are skipped under the narrow mechanical route in METHOD.md. Native unslop, technical-writing, deslop, no-comments, control-ui, create-skill and Opening a PR are unbundled or unavailable. Use direct clear prose, scoped diff cleanup and review, the public WSGI surface and local commit handoff. No unrelated skill source is fetched. Show Me Your Work's TSV template and helper are unbundled, so its documented header is used directly. No raw native transcript exists. Review captured commands and checkpoint artifacts instead. Review uses a fresh same-model helper, not native model diversity.

Lead requested identity is GPT-6.1 Sol with High reasoning. Exact runtime identity and token/usage attestation are unavailable to the lead and recorded as unknown.

# Final checkpoint

Fresh scoped reviewer returned PASS. All requested verification is complete. No production changes were requested by review. Attention limits remain captured-log-only audit and unknown runtime identity/usage. No open product decision remains. Local commit is the final outstanding delivery step.

The verified source change is committed as 89f11c9b5b1725dd3126606fffcb846cf60c61b9. Evidence will be committed separately with REPORT.json referring to that evidence commit by HEAD to avoid a self-referential commit hash.
