# S04 Root-Cause Oracle v0

Status: FROZEN

Scenario: S04-v0

## Injected mechanism

The fixture implementation must contain the equivalent of this lifecycle bug:

A Run that fails an intermediate Attempt and later reaches terminal failure executes failure-alert ownership from two lifecycle paths.

One path incorrectly treats the failed Attempt as alert-worthy terminal work.

A second path correctly emits the terminal Run failure Alert.

The synthetic alert adapter is functioning correctly and should not be globally deduplicated.

## Required fix property

Alert ownership must be aligned with terminal Run lifecycle so that:

- intermediate failed Attempts do not independently emit the terminal Run failure alert;
- terminal failure emits exactly one Alert for that Run;
- a separate failed Run can emit an equivalent Alert without being suppressed.

The exact source-code location may vary with implementation, but the defect mechanism must remain equivalent.

## False fixes evaluator must reject

- deduplicate by message text;
- deduplicate by Job id;
- suppress all but the first alert globally;
- disable retry alerts by changing retry count;
- treat each retry Attempt as a separate Run;
- remove legitimate Alert emission entirely.

## Verification intent

Evaluator cases must include:

1. terminal failure after retry -> exactly one Alert;
2. two separate terminally failed Runs of the same Job -> two Alerts;
3. no-retry terminal failure -> one Alert;
4. successful Run -> no failure Alert;
5. configured retry count remains unchanged.
