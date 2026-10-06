# Skill Anatomy Analysis Template

Use this template when inspecting any skill, playbook, command, runbook, workflow, or capability package.

Source:
Snapshot:
Host/runtime:
Inspection date:

## Trigger

- What activates it?
- What explicitly must not activate it?
- Is invocation explicit, implicit, event-driven, scheduled, or routed by another skill?

## Context

- What facts must already be known?
- What files, docs, runtime state, history, or external data does it load?
- Which context is authoritative?
- What context can be fetched instead of asking the operator?

## Procedure

- What reusable decision process or sequence is encoded?
- Which steps are mandatory vs optional?
- Where can it branch?
- How does it recover when an assumption fails?

## Tools

- Which tools or executable capabilities does it require?
- Which are vendor/host-specific?
- Could the same procedure run through another adapter?

## State

- What must survive during execution?
- What must survive across sessions?
- Where is that state stored?
- Is it inspectable and resumable by another agent?

## Verification

- What is the success predicate?
- Which checks are executable?
- Is verification against the real artifact or a proxy?
- Can the procedure produce a false green?
- Is independent review used?

## Output Contract

- What does the next agent, workflow, or human receive?
- Is that output durable?
- Is enough provenance/evidence attached to trust it?

## Operating properties

- Human interruption policy:
- Reversibility policy:
- Failure/retry behavior:
- Idempotency:
- Composability:
- Expected process overhead:
- Security/privacy considerations:

## Portable principle

Describe the mechanism without naming the current file format, vendor, model, or host.

## Vendor-specific binding

Describe exactly which parts depend on the current host/runtime.

## Hypotheses to test

List falsifiable claims suggested by the static analysis.

## Evidence status

- **Observed:** facts directly supported by inspected source.
- **Hypothesis:** inference requiring experiment.
- **Verified:** reserve for runtime or independently reproducible evidence.
