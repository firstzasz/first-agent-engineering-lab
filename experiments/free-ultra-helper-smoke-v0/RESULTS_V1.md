# Ultra Helper Host V1: observed second role-gate failure

**Execution date:** 2026-10-31 UTC. **Status: LIVE API EXECUTED; HOST CAPABILITY NOT_VERIFIED.**

- [GitHub Actions V1 run #41230695752](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230695752): preflight unit tests **passed**, live-helper job **failed**, no-API independent grader **failed** as designed.
- NVIDIA free hosted `nvidia/nemotron-3-ultra-550b-a55b` returned **HTTP 200** to exactly **one Lead request**, in **12.78 seconds**, with correct requested model ID.
- Lead's expected `submit_plan` tool call **was not emitted**. The runner correctly stopped; Implementer and Reviewer were not invoked.
- No tool-generated code was executed or saved, and no model output/credential was printed.
- V1 changed only the Lead schema to `ack: true` versus V0's `steps: string[1..4]`. All other test conditions and model remained the same.

## Important comparison with frozen V0

| Stage | V0 [run #41230556375](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230556375) | V1 [run #41230695752](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41230695752) |
|---|---|---|
| Model | Ultra 550B | Ultra 550B |
| Lead API | HTTP 200, 6.10s | HTTP 200, 12.78s |
| Expected tool name | **Emitted** | **Not emitted** |
| Lead arguments valid | **No** | Not applicable: no call |
| Implementer request | Not attempted | Not attempted |
| Reviewer request | Not attempted | Not attempted |
| Full helper host VERIFIED | **No** | **No** |

**Interpretation:** Tool-call reliability/argument validity in this structured role-specific interface is unresolved. These two observations are small, stochastic and cannot isolate cause to schema alone; the host also used `tool_choice=auto` and model/infrastructure loading may vary. Avoid inferring a model quality ranking or native multi-agent capability from these one-shots.

## Next proposed protocol, not executed

A new separately frozen V2 host calibration should test exact provider-supported **forced named function choice** (if officially compatible), versus `tool_choice=auto`, using a very small schema, with bounded repetitions and a single-role tool-call success metric. Only after a stable, executable lead-contract calibration should the implementer/reviewer chain be attempted again. No silent retries of V0/V1.

Before scored pstack/Matt/FIRST-mode research, the gate in [METHOD_COMPARISON_GATE.md](https://github.com/firstzasz/first-agent-engineering-lab/blob/research/free-discovery-semantic-evaluator-v1/experiments/free-s02-semantic-v1/METHOD_COMPARISON_GATE.md) remains **BLOCKED**. The existing 18/18 offline unit-test result verifies only mock role, permission and budget boundaries.

No Groq, DeepSeek on NVIDIA, paid models, production changes or `main` merge.
