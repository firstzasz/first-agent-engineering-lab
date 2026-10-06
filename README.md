# FIRST Agent Engineering Lab

Public R&D repository for studying, testing, comparing, adapting, and designing evidence-based AI agent engineering workflows.

The lab exists to learn what actually works before any idea is proposed for FIRST production systems.

## Research loop

observe -> understand -> experiment -> measure -> compare -> document -> propose

Popular or authoritative approaches are inputs, not conclusions. We separate principles, implementation details, vendor-specific behavior, and portable patterns.

## Long-term research thesis

A central research pillar is **skill engineering as reusable procedural knowledge**.

The lab does not assume that `SKILL.md`, any current plugin format, or any current agent host will be permanent. Instead it studies how reusable engineering know-how should be represented across:

```text
Model
  ↓
Context / Knowledge
  ↓
Skills / Procedures
  ↓
Tools / Actions
  ↓
State / Memory
  ↓
Verification
  ↓
Environment
```

The target is to learn what should be a skill, what should be a tool, what should be memory or persistent task state, what should be a larger workflow, and what should be enforced by executable verification rather than prose alone.

See [docs/SKILL_ENGINEERING.md](./docs/SKILL_ENGINEERING.md) and [ADR-0002](./docs/adrs/0002-skill-engineering-as-portable-procedural-knowledge.md).

## Current scope

Phase 0 bootstraps the research system and performs a read-only architecture inspection of:

- Lauren Tan's **pstack**, officially published under `cursor/plugins/pstack`
- Matt Pocock's **skills** repository

No upstream code is copied or modified during bootstrap.

## Repository map

- [RESEARCH_INDEX.md](./RESEARCH_INDEX.md): current research state and next work
- [docs/SKILL_ENGINEERING.md](./docs/SKILL_ENGINEERING.md): long-term skill-engineering research thesis
- [docs/approaches/FIRST_MODE_V0.md](./docs/approaches/FIRST_MODE_V0.md): frozen FIRST-specific experimental operating contract
- [docs/sources/](./docs/sources/): upstream registry and architecture notes
- [docs/experiments/](./docs/experiments/): experiment method and template
- [docs/comparisons/](./docs/comparisons/): comparison plans and results
- [docs/proposals/](./docs/proposals/): candidate patterns for later FIRST review
- [docs/adrs/](./docs/adrs/): research-repository decisions
- [experiments/](./experiments/): executable experiment implementations
- [fixtures/](./fixtures/): synthetic fixtures only
- [AGENTS.md](./AGENTS.md): operating contract for agents working in this repo

## Safety boundary

This repository is public. Never commit production credentials, private endpoints, personal financial records, private user information, OCI credentials, GitHub secrets, or production configuration containing sensitive values.

Experiments must use synthetic data and fake fixtures.

This lab does not modify FIRST Data Hub, market-screener, OCI production services, or real financial data unless a later, explicit production decision authorizes separate work.

## Evidence standard

A statement such as "implemented" means the artifact exists. A statement such as "verified" requires executable or externally inspectable evidence.

Research outcomes graduate through:

research -> experiment -> evidence -> documented proposal -> FIRST architecture review -> production implementation
