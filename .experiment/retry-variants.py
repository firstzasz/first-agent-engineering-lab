from relayboard.service import RunAlreadyTerminal
from relayboard.web import create_seeded_app

app = create_seeded_app()
app.store.add_job("three-tries", "Three tries", max_attempts=3)
for job, outcomes, states, expected_alert_count, terminal in (
    ("daily-report", [False, True], ["retry", "succeeded"], 0, "succeeded"),
    ("three-tries", [False, False, False], ["retry", "retry", "failed"], 1, "failed"),
    ("three-tries", [False, False, False], ["retry", "retry", "failed"], 2, "failed"),
):
    run = app.service.begin_manual_run(job)
    observed = [app.service.record_attempt(run.id, succeeded=result) for result in outcomes]
    assert observed == states, observed
    assert app.store.get_run(run.id).status == terminal
    assert [a.number for a in app.store.list_attempts(run.id)] == ([1, 2] if job == "daily-report" else [1, 2, 3])
    alerts = app.store.list_alerts()
    assert len(alerts) == expected_alert_count, alerts
    try:
        app.service.record_attempt(run.id, succeeded=False)
    except RunAlreadyTerminal:
        pass
    else:
        raise AssertionError("terminal Run accepted extra Attempt")
    assert len(app.store.list_alerts()) == expected_alert_count
    print({"run": run.id, "job": job, "states": observed, "terminal": terminal, "alert_count": len(alerts)})
assert [a.run_id for a in app.store.list_alerts()] == ["run-002", "run-003"]
print("retry variants passed")
