from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(
            f"{path}: expected exactly one frozen-base match; "
            f"found {text.count(old)}"
        )
    path.write_text(text.replace(old, new), encoding="utf-8")


def apply(workspace: Path) -> None:
    relayboard = workspace / "relayboard"

    replace_once(
        relayboard / "models.py",
        """    enabled: bool
    max_attempts: int
""",
        """    enabled: bool
    max_attempts: int
    archived: bool = False
""",
    )

    replace_once(
        relayboard / "store.py",
        """                enabled INTEGER NOT NULL,
                max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1)
            );
""",
        """                enabled INTEGER NOT NULL,
                max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1),
                archived INTEGER NOT NULL DEFAULT 0
            );
""",
    )

    replace_once(
        relayboard / "store.py",
        """        return Job(
            row["id"],
            row["name"],
            bool(row["enabled"]),
            row["max_attempts"],
        )
""",
        """        return Job(
            row["id"],
            row["name"],
            bool(row["enabled"]),
            row["max_attempts"],
            bool(row["archived"]),
        )
""",
    )

    replace_once(
        relayboard / "store.py",
        """        rows = self.connection.execute(
            "SELECT * FROM jobs ORDER BY id"
        ).fetchall()
        return [
            Job(r["id"], r["name"], bool(r["enabled"]), r["max_attempts"])
            for r in rows
        ]
""",
        """        rows = self.connection.execute(
            "SELECT * FROM jobs WHERE archived = 0 ORDER BY id"
        ).fetchall()
        return [
            Job(
                r["id"],
                r["name"],
                bool(r["enabled"]),
                r["max_attempts"],
                bool(r["archived"]),
            )
            for r in rows
        ]
""",
    )

    replace_once(
        relayboard / "store.py",
        """    def set_job_enabled(self, job_id: str, enabled: bool) -> Job:
""",
        """    def set_job_archived(self, job_id: str, archived: bool) -> Job:
        self.get_job(job_id)
        self.connection.execute(
            "UPDATE jobs SET archived = ? WHERE id = ?",
            (int(archived), job_id),
        )
        self.connection.commit()
        return self.get_job(job_id)

    def set_job_enabled(self, job_id: str, enabled: bool) -> Job:
""",
    )

    replace_once(
        relayboard / "service.py",
        """class JobNotSchedulable(RuntimeError):
    pass


class RunAlreadyTerminal(RuntimeError):
""",
        """class JobNotSchedulable(RuntimeError):
    pass


class JobArchived(RuntimeError):
    pass


class RunAlreadyTerminal(RuntimeError):
""",
    )

    replace_once(
        relayboard / "service.py",
        """    def begin_manual_run(self, job_id: str) -> Run:
        self.store.get_job(job_id)
        return self.store.create_run(job_id, "manual")
""",
        """    def begin_manual_run(self, job_id: str) -> Run:
        job = self.store.get_job(job_id)
        if job.archived:
            raise JobArchived(f"job {job_id} is archived")
        return self.store.create_run(job_id, "manual")
""",
    )

    replace_once(
        relayboard / "service.py",
        """        job = self.store.get_job(job_id)
        if not job.enabled:
""",
        """        job = self.store.get_job(job_id)
        if job.archived:
            raise JobNotSchedulable(f"job {job_id} is archived")
        if not job.enabled:
""",
    )

    replace_once(
        relayboard / "service.py",
        """    def set_job_enabled(self, job_id: str, enabled: bool) -> None:
        self.store.set_job_enabled(job_id, enabled)

""",
        """    def set_job_enabled(self, job_id: str, enabled: bool) -> None:
        self.store.set_job_enabled(job_id, enabled)

    def archive_job(self, job_id: str):
        return self.store.set_job_archived(job_id, True)

    def restore_job(self, job_id: str):
        return self.store.set_job_archived(job_id, False)

""",
    )

    replace_once(
        relayboard / "web.py",
        "from .service import JobNotSchedulable, RelayBoardService",
        "from .service import JobArchived, JobNotSchedulable, RelayBoardService",
    )

    replace_once(
        relayboard / "web.py",
        """            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/enabled")
            ):
""",
        """            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/archive")
            ):
                job_id = path.split("/")[3]
                job = self.service.archive_job(job_id)
                return self._json(
                    start_response,
                    200,
                    {"job": self._job_json(job)},
                )

            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/restore")
            ):
                job_id = path.split("/")[3]
                job = self.service.restore_job(job_id)
                return self._json(
                    start_response,
                    200,
                    {"job": self._job_json(job)},
                )

            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/enabled")
            ):
""",
    )

    replace_once(
        relayboard / "web.py",
        """        except JobNotSchedulable as exc:
            return self._json(
                start_response,
                409,
                {"error": str(exc)},
            )

        return self._json(
""",
        """        except JobNotSchedulable as exc:
            return self._json(
                start_response,
                409,
                {"error": str(exc)},
            )
        except JobArchived as exc:
            return self._json(
                start_response,
                409,
                {"error": str(exc)},
            )

        return self._json(
""",
    )

    replace_once(
        relayboard / "web.py",
        """            "max_attempts": job.max_attempts,
        }
""",
        """            "max_attempts": job.max_attempts,
            "archived": job.archived,
        }
""",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()
    apply(Path(args.workspace).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
