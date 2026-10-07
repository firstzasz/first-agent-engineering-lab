# How grounding

Scope is small despite crossing four files. The lead is the declared serial How explainer per METHOD step 3. Bundled native explorer/explainer prompt references are unavailable.

A Job is an immutable dataclass returned by Store from SQLite. Store alone owns job state writes. RelayBoardService controls run admission and completion. begin_scheduled_run currently checks enabled before creating a Run. begin_manual_run bypasses scheduling eligibility. record_attempt rereads Job only for max_attempts and completes the same Run; retry and alert logic must stay unchanged.

The WSGI API delegates commands to the service and serializes Job via one _job_json function. KeyError becomes JSON 404; JobNotSchedulable becomes JSON 409. Mutating Job commands return 200 with a job envelope. Runs return 201. Dashboard reads list_jobs and last terminal Run result. relayboard.testing.request exercises the actual WSGI app with deterministic input.

The injected SQLite connection means existing jobs tables may predate this change. New state should default to unpaused, preserve enabled and historical Runs, and survive Store reopening on that connection. The app has no background scheduler thread or async worker to redesign. Concurrency redesign is outside this task.

The baseline test run passed 5 tests. See baseline.log and commands.jsonl. The glossary explicitly declines to define pause. Operator response supplies manual/current-Run semantics; remaining representation and dashboard decisions are reversible under the preservation requirement.
