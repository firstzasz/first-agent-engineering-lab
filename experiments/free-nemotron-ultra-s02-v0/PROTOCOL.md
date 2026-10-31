# FREE_NEMOTRON_ULTRA_S02_V0 — frozen before execution

Status: **FROZEN PRE-RUN**. Research-only; no production integration, no `main` merge.

## Research question
Does changing **only the NVIDIA hosted free model** from `openai/gpt-oss-20b` to `nvidia/nemotron-3-ultra-550b-a55b` improve implementation, requirement elicitation and verification of the frozen S02-v0.1 task in the same four single-agent proxy methodology arms?

## Source and declared controls
- Prior cohort: [Free S02 four-arm screen V0](https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41211207214), which attempted four NVIDIA GPT-OSS 20B arms and four OpenRouter Nemotron Lightning arms.
- Reused exact code: `experiments/free-s02-screen-v0/screen.py`, `experiments/free-s02-screen-v0/grade.py`, `experiments/free-s02-screen-v0/inside_grade.py`.
- Same frozen RelayBoard fixture SHA: `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.
- Same frozen scenario S02-v0.1; same frozen evaluator and operator answer sheet.
- Four arms and exact order: **Matt proxy → Neutral → FIRST proxy → pstack proxy**.
- Preserved non-native port sources from `226a03a883c65c81223ca49e00ddd058e1b38691`. **These are not the native full pstack or Matt Pocock implementations.**
- Same API request cap **9** per arm, output token limit **3000** per request, HTTP timeout **90s**, file read/write limits and fixed tool declarations.
- **New model only:** NVIDIA `nvidia/nemotron-3-ultra-550b-a55b`; no other source/method/evaluator/fixture changes authorized within this cohort.
- No auto-retry on failed inference, no paid fallback, Groq and NVIDIA-hosted DeepSeek excluded; use existing `NVIDIA_API_KEY` from trusted GitHub Actions Secrets.

## Staged execution
1. Run exactly **one** small synthetic tool-call preflight on the Ultra endpoint, which confirms free API connectivity and callable-function response shape. If unsuccessful, stop and preserve evidence without starting four-arm cohort. No silent fallback.
2. If passed, execute four full S02 contestant arms serially with fresh independent fixture contexts and a maximum of **36 S02 model calls**. New protocol model ID is recorded in every run's `result.json`.
3. After all contestants terminate, an evaluator job **without API secrets** checks candidate integrity, unchanged public tests and frozen S02 evaluator in a Docker container with no network and restricted permissions.
4. Preserve all run dispositions, including partial implementations, malformed tool calls and expected suite failures. Never feed hidden evaluator output back into the same contestant.

## Interpretation and billing
NVIDIA's hosted model catalog advertises `nvidia/nemotron-3-ultra-550b-a55b` as a free prototype endpoint. Community reports suggest a 40 RPM limit for some NIM developer accounts, but NVIDIA says limits depend on the model and traffic. **40 RPM does not guarantee this model will always respond or provide an unlimited total quota.** The workflow makes requests serially, has no paid endpoint and stops on 429 per frozen policy. The operator's account-specific remaining entitlement is unknown until endpoint response.

A result on one run per arm is a **screen** and is not a causal/replication proof. The only intentional changed axis is model identity; host-side stochasticity, load, free-tier availability, and latency are uncontrolled. No model/method universal winner may be declared.

## Risk and evidence boundary
The original S02 driver retains restricted read/write tool paths and executes synthetic code only in an offline Docker container, without Keys. The grader has no NVIDIA Secret. No arbitrary shell is offered to the contestant. GitHub artifacts are temporary; record a durable results digest in the research branch and Issue #40 after execution.

Protocol frozen and no S04 or EXP-0017 C2 execution authorized by this cohort.
