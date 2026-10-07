from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    id: str
    name: str
    enabled: bool
    max_attempts: int


@dataclass(frozen=True)
class Run:
    id: str
    job_id: str
    source: str
    status: str


@dataclass(frozen=True)
class Attempt:
    run_id: str
    number: int
    succeeded: bool


@dataclass(frozen=True)
class Alert:
    id: int
    run_id: str
    job_id: str
    kind: str
    message: str
