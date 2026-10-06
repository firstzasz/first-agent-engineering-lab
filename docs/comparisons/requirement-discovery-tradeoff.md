# Requirement Discovery Tradeoff: pstack vs Matt Pocock

Status: STATIC INTERPRETATION, runtime validation pending

Date: 2026-10-06

Pinned sources:

- pstack: `df581122cde17e6e27686b5a448bde23e4ad4318`
- Matt Pocock skills: `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`

## Question

If combining Matt-style requirement discovery with pstack-style autonomy looks attractive, did pstack simply overlook requirement discovery?

## What the source actually shows

No. The pstack source already contains an explicit question-classification policy.

`poteto-mode` says that before asking the operator a design/approach question, the agent should classify it:

- if the answer is empirically observable, investigate or prototype rather than ask;
- if a full-autonomy grant covers the call, decide and act;
- if only the operator can make the call, apply a default under the grant and explain it;
- genuine product/preference decisions remain operator decisions;
- named gates and irreversible actions still pause.

The Feature playbook says the agent **owns the design**, grounds the subsystem with `how`, runs `architect`, and proceeds through implementation and verification.

The Architect skill defaults to proceeding from synthesized design to implementation without a human checkpoint. A checkpoint is opt-in when explicitly requested.

The Prototype playbook does involve the user when the open question is genuinely experiential or directional, such as choosing between visual directions.

Matt Pocock's `grilling` skill makes a different default:

- facts are the agent's job;
- decisions are the user's;
- decisions are represented as a dependency-aware design tree;
- every currently-unblocked decision is presented to the user in rounds;
- execution waits until the design frontier is empty and shared understanding is confirmed.

## Static interpretation

The difference is therefore not "one understands requirements and the other forgot."

It is primarily a difference in **default locus of authority** and **cost function**.

### pstack default

Optimize for agent ownership, throughput, and low operator blocking.

A capable agent should resolve facts empirically, make reversible engineering calls, and only escalate genuine human decisions.

This minimizes interaction cost but accepts the risk that the agent may choose a technically reasonable design that is not the operator's preferred product intent unless that intent was already explicit.

### Matt default

Optimize for alignment and explicit shared understanding before execution.

The agent discovers facts, but it deliberately surfaces the design decisions themselves to the operator.

This reduces silent product assumptions but increases operator interaction and can impose ceremony on work where the operator is comfortable delegating those choices.

## Why both defaults can be rational

They appear to target different dominant failure modes:

- **pstack failure model:** agents stall, ask too much, over-coordinate with humans, or fail to drive work to verified completion.
- **Matt failure model:** agents confidently build the wrong thing because the human and agent never made the implicit product/design decisions explicit.

These are not mutually exclusive failure modes. The ideal balance can depend on task type and operator style.

## FIRST hypothesis

A promising FIRST policy is not simply "Matt discovery + pstack autonomy."

It is a three-way decision policy:

1. **Fact / empirically observable:** agent investigates.
2. **Reversible engineering choice inside the granted goal:** agent decides, records rationale, and continues.
3. **Product/preference choice that changes desired behavior:** operator decides.

Hard security or irreversible gates remain explicit approvals.

This is a hypothesis. S02 in the RelayBoard benchmark should test whether this policy reduces operator interruptions without increasing silent requirement errors.

## What remains unknown

Static source inspection cannot tell us:

- how often pstack's agent-owned design makes unwanted product assumptions in practice;
- how often Matt's decision-frontier interaction catches meaningful ambiguity rather than creating overhead;
- where the best threshold lies for FIRST-style work;
- whether stronger models shift that threshold over time.

These require controlled runtime experiments.
