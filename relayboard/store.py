from __future__ import annotations

import sqlite3

from .models import Alert, Attempt, Job, Run


class Store:
    def __init__(self, connection: sqlite3.Connection | None = None) -> None:
        self.connection = connection or sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                enabled INTEGER NOT NULL,
                max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1),
                paused INTEGER NOT NULL DEFAULT 0 CHECK(paused IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL REFERENCES jobs(id),
                source TEXT NOT NULL CHECK(source IN ('manual', 'scheduled')),
                status TEXT NOT NULL CHECK(status IN ('running', 'succeeded', 'failed'))
            );
            CREATE TABLE IF NOT EXISTS attempts (
                run_id TEXT NOT NULL REFERENCES runs(id),
                number INTEGER NOT NULL,
                succeeded INTEGER NOT NULL,
                PRIMARY KEY (run_id, number)
            );
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL REFERENCES runs(id),
                job_id TEXT NOT NULL REFERENCES jobs(id),
                kind TEXT NOT NULL,
                message TEXT NOT NULL
            );
            """
        )
        columns = {
            row["name"]
            for row in self.connection.execute("PRAGMA table_info(jobs)")
        }
        if "paused" not in columns:
            self.connection.execute(
                "ALTER TABLE jobs ADD COLUMN paused INTEGER NOT NULL "
                "DEFAULT 0 CHECK(paused IN (0, 1))"
            )
        self.connection.commit()

    def add_job(
        self,
        job_id: str,
        name: str,
        *,
        enabled: bool = True,
        max_attempts: int = 1,
        paused: bool = False,
    ) -> Job:
        self.connection.execute(
            "INSERT INTO jobs(id, name, enabled, max_attempts, paused) "
            "VALUES (?, ?, ?, ?, ?)",
            (job_id, name, int(enabled), max_attempts, int(paused)),
        )
        self.connection.commit()
        return self.get_job(job_id)

    def get_job(self, job_id: str) -> Job:
        row = self.connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,),
        ).fetchone()
        if row is None:
            raise KeyError(job_id)
        return Job(
            row["id"],
            row["name"],
            bool(row["enabled"]),
            row["max_attempts"],
            bool(row["paused"]),
        )

    def list_jobs(self) -> list[Job]:
        rows = self.connection.execute(
            "SELECT * FROM jobs ORDER BY id"
        ).fetchall()
        return [
            Job(
                r["id"], r["name"], bool(r["enabled"]),
                r["max_attempts"], bool(r["paused"]),
            )
            for r in rows
        ]

    def set_job_enabled(self, job_id: str, enabled: bool) -> Job:
        self.get_job(job_id)
        self.connection.execute(
            "UPDATE jobs SET enabled = ? WHERE id = ?",
            (int(enabled), job_id),
        )
        self.connection.commit()
        return self.get_job(job_id)

    def set_job_paused(self, job_id: str, paused: bool) -> Job:
        self.get_job(job_id)
        self.connection.execute(
            "UPDATE jobs SET paused = ? WHERE id = ?",
            (int(paused), job_id),
        )
        self.connection.commit()
        return self.get_job(job_id)

    def next_run_id(self) -> str:
        row = self.connection.execute(
            "SELECT COUNT(*) AS n FROM runs"
        ).fetchone()
        return f"run-{row['n'] + 1:03d}"

    def create_run(self, job_id: str, source: str) -> Run:
        self.get_job(job_id)
        run_id = self.next_run_id()
        self.connection.execute(
            "INSERT INTO runs(id, job_id, source, status) VALUES (?, ?, ?, 'running')",
            (run_id, job_id, source),
        )
        self.connection.commit()
        return self.get_run(run_id)

    def get_run(self, run_id: str) -> Run:
        row = self.connection.execute(
            "SELECT * FROM runs WHERE id = ?",
            (run_id,),
        ).fetchone()
        if row is None:
            raise KeyError(run_id)
        return Run(
            row["id"],
            row["job_id"],
            row["source"],
            row["status"],
        )

    def set_run_status(self, run_id: str, status: str) -> Run:
        self.get_run(run_id)
        self.connection.execute(
            "UPDATE runs SET status = ? WHERE id = ?",
            (status, run_id),
        )
        self.connection.commit()
        return self.get_run(run_id)

    def add_attempt(self, run_id: str, succeeded: bool) -> Attempt:
        self.get_run(run_id)
        row = self.connection.execute(
            "SELECT COUNT(*) AS n FROM attempts WHERE run_id = ?",
            (run_id,),
        ).fetchone()
        number = row["n"] + 1
        self.connection.execute(
            "INSERT INTO attempts(run_id, number, succeeded) VALUES (?, ?, ?)",
            (run_id, number, int(succeeded)),
        )
        self.connection.commit()
        return Attempt(run_id, number, succeeded)

    def list_attempts(self, run_id: str) -> list[Attempt]:
        rows = self.connection.execute(
            "SELECT * FROM attempts WHERE run_id = ? ORDER BY number",
            (run_id,),
        ).fetchall()
        return [
            Attempt(r["run_id"], r["number"], bool(r["succeeded"]))
            for r in rows
        ]

    def add_alert(
        self,
        run_id: str,
        job_id: str,
        kind: str,
        message: str,
    ) -> Alert:
        cur = self.connection.execute(
            "INSERT INTO alerts(run_id, job_id, kind, message) VALUES (?, ?, ?, ?)",
            (run_id, job_id, kind, message),
        )
        self.connection.commit()
        return Alert(cur.lastrowid, run_id, job_id, kind, message)

    def list_alerts(self) -> list[Alert]:
        rows = self.connection.execute(
            "SELECT * FROM alerts ORDER BY id"
        ).fetchall()
        return [
            Alert(
                r["id"],
                r["run_id"],
                r["job_id"],
                r["kind"],
                r["message"],
            )
            for r in rows
        ]

    def last_result_for_job(self, job_id: str) -> str | None:
        row = self.connection.execute(
            """
            SELECT status
            FROM runs
            WHERE job_id = ? AND status != 'running'
            ORDER BY rowid DESC
            LIMIT 1
            """,
            (job_id,),
        ).fetchone()
        return None if row is None else row["status"]
