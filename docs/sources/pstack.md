# Source Inspection: Lauren Tan / pstack

Snapshot: `df581122cde17e6e27686b5a448bde23e4ad4318`  
Observed plugin version: `0.15.15`  
License: MIT, Copyright (c) 2026 Lauren Tan

Official source: `https://github.com/cursor/plugins/tree/main/pstack`

## What was inspected

Read-only inspection covered the plugin manifest, README, root layout, skill inventory, agent inventory, automation directory, `poteto-mode`, and representative skills/playbooks for setup, architecture, TDD, swarming, decision trails, autonomous work, orchestration, and session pickup.

No pstack source was copied into this lab.

## Observed architecture

The upstream package is a Cursor plugin with these major surfaces:

- `.cursor-plugin/`: plugin metadata and host packaging.
- `skills/`: a large set of workflow skills plus engineering-principle skills.
- `skills/poteto-mode/`: a higher-order router that selects task-specific playbooks and composes other skills.
- `agents/`: specialized subagents, including a general pstack delegate and a focused comment-review agent.
- `automations/`: optional automation material.
- `docs/` and `assets/`: user-facing documentation and plugin assets.

The manifest explicitly points Cursor at `skills/` and `agents/`.

## Workflow shape observed

`poteto-mode` is the central orchestration layer. Its README describes playbooks for investigation, bug fixing, performance work, feature work, refactoring, prototypes, evaluation, PR babysitting/shipping, autonomous runs, orchestration, session pickup, safe pause, multi-phase planning, and PR opening.

Representative observations:

- **Requirement and problem discovery:** `how`, `why`, prototype rules, and premise-challenging principles push the agent to inspect facts before asking the operator to decide empirical questions.
- **Architecture:** `architect` separates grounding, sketching, optional agreement, implementation, and redesign when the shape is wrong.
- **Execution:** playbooks define ordered steps and route into specialist skills.
- **Verification:** explicit verification skills and principles emphasize proving behavior rather than reporting completion.
- **Session continuity:** dedicated session-pickup and pause-safely playbooks exist.
- **Autonomy:** autonomous-run and orchestrate playbooks are first-class concepts rather than incidental prompt wording.
- **Multi-agent work:** `swarm`, `arena`, and adversarial review patterns are built into the workflow surface.
- **Auditability:** `show-me-your-work` defines a structured decision trail for long or unattended work.
- **Host configuration:** `setup-pstack` maps available models and reasoning budgets to roles.

## Vendor-specific surfaces observed

The official distribution is a Cursor plugin and several workflows rely on Cursor concepts such as plugin manifests, model selection, persistent modes, subagents, or host commands.

That does not prove the engineering principles are Cursor-specific. It means portability must be tested by separating the principle from the host binding.

## Hypotheses for Phase 1

These are not verified results:

1. A higher-order playbook router may improve autonomy and reduce ad-hoc execution drift on long tasks.
2. Explicit decision trails may improve handoff and reviewability at the cost of extra process overhead.
3. The largest portability cost may live in orchestration and host bindings, not in the underlying engineering principles.

Runtime behavior has not yet been tested by this lab.
