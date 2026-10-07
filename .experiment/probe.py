from relayboard.web import create_seeded_app
app = create_seeded_app()
run = app.service.begin_manual_run("daily-report")
for _ in range(2):
    result = app.service.record_attempt(run.id, succeeded=False)
    print({"boundary": "record_attempt return", "return": result, "run_status": app.store.get_run(run.id).status, "attempt_numbers": [a.number for a in app.store.list_attempts(run.id)], "alert_count": len(app.store.list_alerts())})
