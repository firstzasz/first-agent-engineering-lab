# Feature steps copied from bundled playbook
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

# Status and port bindings
1. Complete. Lead serial How tracing under METHOD step 3. See grounding.md.
2. Complete. Two serial lead sketches and synthesis under METHOD. See design.md.
3. Complete. Four throughput items recorded before implementation. See throughput.md.
4. Complete. Fresh serial helper implemented tests and code; separate fresh reviewer finished.
5. Complete. Lead original WSGI API scenario, 10 focused and 15 full public tests pass. Reviewer preexisting legacy-history check passes.
6. Complete. Tests-only 087535a then implementation b04219d on existing isolated branch. No rebase to unassigned branch needed.
7. Skip. Design not contested; interrogate is unbundled and was not fetched.
8. Port handoff. Native PR route unbundled. METHOD replaces it with local immutable candidate and evidence commit handed to orchestrator; no remote operation.

# Architect phases
1. Ground. Complete. See grounding.md.
2. Sketch. Complete. Two structurally distinct serial lead sketches in design.md.
3. Agree. Skip opt-in human checkpoint; no request for design approval.
4. Implement. Complete. Candidate b04219d with verified public behavior.
5. Scrap. n/a. Sketch fit implementation; exact route correction did not require redesign.

# Arena design phases
1. Frame. Complete. Task, usage and rubric in design.md.
2. Fan out. Port uses serial lead sketches, no native fan-out.
3. Cross-judge. Native arena step replaced by lead synthesis and finished fresh same-model final review per METHOD; no native cross-model judgement.
4. Pick. Complete. Independent Job state selected in design.md.
5. Graft. n/a. No useful relation-table graft into chosen Job shape.
6. Verify. Complete. Lead and fresh reviewer checked original surface and public evidence.
