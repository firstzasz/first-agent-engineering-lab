# Gate for the real four-way engineering-method experiment

**Status: DESIGN / NOT YET EXECUTED.** This gate describes the next user-requested comparison:
**Neutral vs pstack vs Matt Pocock Skills vs FIRST-mode**. It must not be confused with G0/G1/G2/G3 discovery-mechanism runs.

## Frozen source identities

| Arm | Source | Version/grounding | Must demonstrate |
|---|---|---|---|
| Neutral | Common host instructions only | S02 pilot fixture pinned `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f` | Normal inspect/edit/test/diff cycle; same operator and limits |
| pstack | Pinned Codex port + bundled upstream Poteto Mode + matching playbooks | `PSTACK_CODEX_PORT_V0.md` at `226a03a883c65c81223ca49e00ddd058e1b38691`; upstream `cursor/plugins/pstack` `df581122...` | Actual read of assigned skill files; classifications/throughput; bounded fresh implementation helper and separate review; evidence trail |
| Matt Pocock Skills | Pinned Codex port + bundled `grill-with-docs`, `to-spec`, TDD, two-axis review | `MATT_CODEX_PORT_V0.md` at same port SHA; upstream `mattpocock/skills` `4588b32...` | Source skill invocation, actual dependency-question step; spec/ticket route when needed; test-first behavior; separate Standards and Spec review contexts |
| FIRST-mode v0 | Frozen FIRST treatment | `docs/approaches/FIRST_MODE_V0.md` at `2b2e67c...` | Ground facts, classify authority, ask for product policy, verify executable results, record evidence and state; avoid pointless helper fan-out |

**Critical fidelity gate:** Merely copying a methodology Markdown file into a system prompt is **not** equivalent to performing its workflow. If tool host cannot execute required stages, label it **NON_NATIVE_PROXY** and do not rank it against a faithful native method as though equivalent. Either implement bounded helper sessions with clean contexts or explicitly narrow the research claim to portable pieces.

## Shared harness requirements before scored inference

- Fixed **single model/provider first**: NVIDIA hosted free `nvidia/nemotron-3-ultra-550b-a55b`, with account entitlement checked; optionally replicate later on OpenRouter `:free`, without cross-provider causal claims. No NVIDIA DeepSeek, Groq, paid fallback, or paid models.
- Fresh independent contestant workspaces; same pinned S02 task, initial fixture commit, public tools and hidden grader; no oracle files or peer answers in contestant context. Repeated seeds, arm order, and stopping budget declared in advance.
- All arms get the same operator interface. Operator resolves the four *policy contrasts* but does not volunteer an answer. Do **not** use legacy broad matcher as primary semantic scorer. Include V1 manual adjudication with blinded independent review or mark discovery outcome `UNADJUDICATED`.
- Actual function tools for source reading, bounded edits, executing public tests in network-disabled container, inspecting real diff, asking operator, and committing persistent result. Tool-protocol names tested against model with synthetic preflight; malformed names and partial arguments recorded.
- pstack/Matt faithful portability needs helper-agent interface with **fresh separate model contexts**, restricted allowlisted file roles, explicit helper input/output, independent read-only review, and a trace proving the helper actually ran. All helper calls consume the **same fixed total model-call/token budget** as other methods; record overhead separately. No hidden-model feedback.
- Verification means **public regression tests + frozen S02 oracle + legitimate decision asking**. Persist code candidate hashes, tool trace, public and hidden evaluator outcomes, required method-stage evidence, duplicate/irrelevant question burden and latency/token usage. A green Workflow job alone never means success.
- Running model-produced code must be sandboxed (Docker with network disabled, no model credentials, read-only fixture mounts except narrow scratch target, non-root/dropped capabilities, finite CPU/memory/time).
- Quota is a separate ceiling from RPM. Enforce serial calls or an explicit RPM budget, 429 -> `QUOTA_BLOCKED`, 5xx -> provider incident, no stealth retry. As of prior Ultra test, one Matt proxy arm stopped with HTTP 500; retain this as infrastructure outcome.

## Missing components at this freeze

The existing `experiments/free-s02-screen-v0/screen.py` is a **single-agent proxy**. Its synthetic tools do not implement actual helper/subagent execution, native skill loading, two-axis fresh review sessions, or meaningful method-stage verification. Its V0 scoring also depended on an invalid semantic decision matcher.

Therefore **READINESS = BLOCKED FOR A FULL-METHOD CAUSAL CLAIM**. It is permissible to implement an isolated host-calibration workflow with fake data and zero inference, but **do not launch a 4-arm scored full-method competition using the current proxy and call the result a victory**.

## Suggested bounded development order

1. Add a normalized helper protocol to the research-only harness with a 1-helper fake scripted fixture, then a real free-model smoke test, instrument token budget and trace. This itself is not a scored methodology trial.
2. Bind/read pinned pstack/Matt upstream skill files through the tool interface, rather than injecting the entire port description and skipping required steps. Validate source hashes.
3. Add a non-leaky operator policy interface with V1 contrast rubric, and build anonymized review packets from questions.
4. Pass host acceptance with synthetic fixture and adversarial injected bad tool calls.
5. Freeze a new *matched* scored S02 cohort at fixed model, request and helper budgets; then extend to S04 bug diagnosis with separate oracle. Report findings by method fidelity and scenario, with failed and quota-blocked cells preserved.

Nothing in this gate authorizes EXP-0017 C2, FIRST-mode production adoption or a merge into `main`.
