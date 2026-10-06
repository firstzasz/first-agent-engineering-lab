# Agent Operating Contract

This repository is an R&D lab, not a production repository.

## Source of truth

GitHub is the persistent source of truth. Do not rely on chat history as the only record of findings, decisions, experiment state, or evidence.

Keep `RESEARCH_INDEX.md`, source notes, experiment records, comparisons, proposals, and ADRs current enough that another agent can resume without the previous chat.

## Research method

Prefer:

observe -> understand -> experiment -> measure -> compare -> document -> propose

Do not copy an upstream technique merely because its author or repository is respected. Inspect the implementation and test the idea.

Separate:

- principle
- implementation
- vendor-specific behavior
- portable pattern

Label hypotheses as hypotheses. Do not present an untested inference as a verified result.

## Experiment discipline

Where practical, every experiment records:

- hypothesis
- setup
- implementation
- expected behavior
- observed behavior
- evidence
- limitations
- result
- recommendation

Failures are valid results.

## Verification

Do not treat an agent saying "done" as proof. Prefer automated tests, CI, integration tests, runtime checks, generated artifacts, reproducible fixtures, benchmark results, and inspectable GitHub state.

Use the words IMPLEMENTED and VERIFIED deliberately and separately.

## Safety

This is a public repository. Use synthetic data and fake fixtures.

Never commit passwords, API tokens, private keys, OCI credentials, GitHub secrets, private endpoints, personal financial records, portfolio transactions, private user information, or production configuration with sensitive values.

Do not modify FIRST Data Hub, market-screener, OCI production services, production credentials, or real financial data from this lab unless explicitly instructed in a later production-scoped task.

## Upstream strategy

Keep upstream sources pristine during initial study. Record exact upstream URLs, SHAs, licenses, and check dates in `docs/sources/registry.yaml`.

Prefer substantial experiments in this FIRST-owned repository rather than heavily mutating upstream forks.

## Integration gate

Promising findings must become evidence and a documented proposal or ADR before they can be considered for FIRST production architecture.
