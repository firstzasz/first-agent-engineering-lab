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
        relayboard / "store.py",
        "status TEXT NOT NULL CHECK(status IN ('running', 'succeeded', 'failed'))",
        "status TEXT NOT NULL CHECK(status IN "
        "('running', 'succeeded', 'failed', 'cancelled'))",
    )

    replace_once(
        relayboard / "service.py",
        """class RunAlreadyTerminal(RuntimeError):
    pass


class RelayBoardService:
""",
        """class RunAlreadyTerminal(RuntimeError):
    pass


class RunCancelled(RuntimeError):
    pass


class RunNotCancellable(RuntimeError):
    pass


class RelayBoardService:
""",
    )

    replace_once(
        relayboard / "service.py",
        """    def record_attempt(self, run_id: str, *, succeeded: bool) -> str:
        run = self.store.get_run(run_id)
        if run.status != "running":
            raise RunAlreadyTerminal(run_id)
""",
        """    def cancel_run(self, run_id: str) -> Run:
        run = self.store.get_run(run_id)
        if run.status == "cancelled":
            return run
        if run.status != "running":
            raise RunNotCancellable(run_id)
        return self.store.set_run_status(run_id, "cancelled")

    def record_attempt(self, run_id: str, *, succeeded: bool) -> str:
        run = self.store.get_run(run_id)
        if run.status == "cancelled":
            raise RunCancelled(run_id)
        if run.status != "running":
            raise RunAlreadyTerminal(run_id)
""",
    )

    replace_once(
        relayboard / "web.py",
        "from .service import JobNotSchedulable, RelayBoardService",
        "from .service import (\n"
        "    JobNotSchedulable,\n"
        "    RunCancelled,\n"
        "    RunNotCancellable,\n"
        "    RelayBoardService,\n"
        ")",
    )

    replace_once(
        relayboard / "web.py",
        """            if (
                method == "POST"
                and path.startswith("/api/runs/")
                and path.endswith("/attempts")
            ):
""",
        """            if (
                method == "POST"
                and path.startswith("/api/runs/")
                and path.endswith("/cancel")
            ):
                run_id = path.split("/")[3]
                run = self.service.cancel_run(run_id)
                return self._json(
                    start_response,
                    200,
                    {"run": run.__dict__},
                )

            if (
                method == "POST"
                and path.startswith("/api/runs/")
                and path.endswith("/attempts")
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
        except (RunCancelled, RunNotCancellable) as exc:
            return self._json(
                start_response,
                409,
                {"error": str(exc)},
            )

        return self._json(
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
