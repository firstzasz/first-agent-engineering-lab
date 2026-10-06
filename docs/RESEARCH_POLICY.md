# Research Policy

## Public repository rule

Assume every committed byte is permanently public.

Use synthetic fixtures only. Do not use production secrets, private financial data, private user information, OCI credentials, or private endpoints.

## Production isolation

The lab may study patterns relevant to FIRST systems, but it does not change FIRST Data Hub, market-screener, OCI production services, production configuration, or real financial data.

A promising pattern must pass through research, experiment, evidence, proposal, architecture review, and only then a separate production implementation decision.

## Evidence hierarchy

Prefer, in descending order:

1. reproducible automated or runtime evidence
2. inspectable GitHub state and exact commit references
3. captured experiment artifacts
4. documented observation
5. hypothesis

Agent narration is not verification by itself.

## Upstream handling

During initial architecture inspection, do not copy or modify upstream source. Record provenance first.

If a later experiment needs upstream material, pin the exact snapshot and preserve license and attribution requirements.
