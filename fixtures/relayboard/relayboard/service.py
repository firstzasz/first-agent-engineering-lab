from __future__ import annotations

from .models import Run
from .store import Store


class JobNotSchedulable(RuntimeError):
    pass


class RunAlreadyTerminal(RuntimeError):
    pass


class RelayBoardService:
    def __init__(self, store: Store) -> None:
        self.store = store

    def begin_manual_run(self, job_id: str) -> Run:
        self.store.get_job(job_id)
        return self.store.create_run(job_id, "manual")

    def begin_scheduled_run(self, job_id: str) -> Run:
        job = self.store.get_job(job_id)
        if not job.enabled:
            raise JobNotSchedulable(f"job {job_id} is disabled")
        return self.store.create_run(job_id, "scheduled")

    def set_job_enabled(self, job_id: str, enabled: bool) -> None:
        self.store.set_job_enabled(job_id, enabled)

    def record_attempt(self, run_id: str, *, succeeded: bool) -> str:
        run = self.store.get_run(run_id)
        if run.status != "running":
            raise RunAlreadyTerminal(run_id)

        job = self.store.get_job(run.job_id)
        attempt = self.store.add_attempt(run_id, succeeded)

        if succeeded:
            self.store.set_run_status(run_id, "succeeded")
            return "succeeded"

        if attempt.number < job.max_attempts:
            self._emit_failure_alert(run_id)
            return "retry"

        self.store.set_run_status(run_id, "failed")
        self._emit_failure_alert(run_id)
        return "failed"

    def _emit_failure_alert(self, run_id: str) -> None:
        run = self.store.get_run(run_id)
        job = self.store.get_job(run.job_id)
        self.store.add_alert(
            run.id,
            job.id,
            "run_failed",
            f"Job {job.name} failed for run {run.id}",
        )
