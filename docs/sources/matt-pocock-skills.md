# Source Inspection: Matt Pocock / skills

Snapshot: `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`  
Observed plugin version: `1.3.1`  
License: MIT, Copyright (c) 2026 Matt Pocock

Official source: `https://github.com/mattpocock/skills`

## What was inspected

Read-only inspection covered the root layout, README, AGENTS.md, Claude plugin manifest, engineering skill inventory, and representative skills for grilling, specification, ticket decomposition, implementation, debugging, TDD, code review, large-work planning, and handoff.

No Matt Pocock skill source was copied into this lab.

## Observed architecture

The repository separates concerns across:

- `skills/engineering/`: promoted engineering workflows.
- `skills/productivity/`: promoted non-code workflows.
- `skills/in-progress/`, `skills/misc/`, and `skills/deprecated/`: lifecycle/status buckets.
- `.claude-plugin/`: Claude Code plugin packaging.
- `.agents/`: agent-facing conventions, installation material, and ADRs.
- `docs/`: human-facing documentation.
- `scripts/`: maintenance and linking helpers.
- `AGENTS.md`: repository invariants and authoring rules.

The upstream explicitly distinguishes user-invoked skills from model-invoked skills.

## Workflow shape observed

A recognizable engineering flow emerges from the promoted skills:

`grill-with-docs -> to-spec -> to-tickets -> implement / implement-spec -> code-review -> PR`

Representative observations:

- **Requirement discovery:** `grill-with-docs` uses an intensive interview and updates durable domain/decision documentation while clarifying the work.
- **Specification:** `to-spec` turns established conversation context into a structured spec rather than re-interviewing.
- **Task decomposition:** `to-tickets` models work as tracer-bullet tickets with explicit blocking edges.
- **Execution:** `implement-spec` treats tickets as a dependency graph, executes the ready frontier with implementer subagents, and merges through an integration branch.
- **Debugging:** `diagnosing-bugs` builds and tightens a feedback loop, reproduces/minimizes, forms hypotheses, instruments, fixes, and adds regression evidence.
- **Verification:** TDD plus a two-axis code review separates repository standards from fidelity to the originating spec.
- **Session continuity:** `handoff` compacts context for another agent; `wayfinder` externalizes large multi-session work as a persistent decision map.
- **Multi-agent work:** implementation and review workflows explicitly delegate parallel subagents and communicate via durable context pointers.
- **Portability claim:** the README describes Claude Code plugin installation and file-based installation for Codex and other agents.

## Vendor-specific surfaces observed

The repository contains a Claude plugin distribution, but the skills are also represented as ordinary files and the upstream documents installation for other agents.

The portability claim is upstream documentation, not yet a lab-verified result. We still need to measure semantic degradation, host assumptions, setup friction, and any required rewrites.

## Hypotheses for Phase 1

These are not verified results:

1. Persisting glossary, ADR, spec, and ticket state may improve session continuity and reduce repeated discovery.
2. Dependency-graph ticketing may improve parallel throughput when tasks contain genuine independent fronts.
3. Small composable skills may be easier to transplant across hosts than a single orchestration-heavy mode, but may require more operator skill to compose correctly.

Runtime behavior has not yet been tested by this lab.
