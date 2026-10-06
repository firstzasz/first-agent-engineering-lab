# Evaluator Protocol v0

Status: FROZEN FOR PILOT

Date frozen: 2026-10-06

## Purpose

Keep treatment inputs stable and preserve evaluator evidence without pretending a public repository can provide cryptographic secrecy.

## Workspace isolation

A treatment agent receives:

- the frozen RelayBoard fixture checkout;
- the scenario prompt;
- the methodology treatment instructions;
- normal tools allowed for that treatment.

A treatment agent does not receive:

- `experiments/relayboard/evaluator/`;
- hidden acceptance cases;
- the S02 operator answer sheet;
- the S04 root-cause oracle.

The evaluator material remains in the lab repository for reproducibility but must not be mounted into the treatment workspace.

If a treatment deliberately fetches evaluator files from the public repository, mark the run **CONTAMINATED** and exclude it from outcome comparison.

## Operator simulation

For S02, the evaluator acts as the operator.

When the treatment asks a valid PRODUCT_OR_PREFERENCE question, the evaluator answers only the requested decision using the frozen answer sheet.

The evaluator must not volunteer additional product requirements.

Questions classed as FACT or REVERSIBLE_ENGINEERING do not receive product guidance. They are recorded as operator burden.

## Evidence capture

For every run preserve:

- treatment name and version;
- model and host;
- starting commit;
- exact prompt;
- tool/action log where available;
- operator questions and answers;
- commits/diff;
- public test output;
- evaluator test output;
- declared completion status;
- checkpoints or handoff artifacts;
- timing/token/tool counts where measurable.

## Contamination and invalid runs

Mark a run invalid when:

- evaluator material was inspected by the treatment;
- start state differs;
- prompt differs;
- oracle or scoring changed after the run began;
- a host failure prevents a comparable execution;
- the agent receives information unavailable to another arm outside the treatment itself.

Do not silently discard failures. Preserve them and label the reason.

## Repeats

A single run is not enough to establish a stable model effect.

Pilot runs may be single-shot to validate the harness. Claims about methodology quality require repeated runs or an explicit limitation.

## Subjective review

Any maintainability or rationale-quality review should be blind to treatment label where practical.

Machine-checkable results take precedence over subjective preference.
