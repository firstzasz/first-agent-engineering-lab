from __future__ import annotations

import json
from io import BytesIO
from wsgiref.util import setup_testing_defaults


def request(
    app,
    method: str,
    path: str,
    payload: dict | None = None,
) -> tuple[int, dict | str]:
    environ: dict = {}
    setup_testing_defaults(environ)
    environ["REQUEST_METHOD"] = method.upper()
    environ["PATH_INFO"] = path

    raw = b""
    if payload is not None:
        raw = json.dumps(payload).encode("utf-8")
        environ["CONTENT_TYPE"] = "application/json"

    environ["CONTENT_LENGTH"] = str(len(raw))
    environ["wsgi.input"] = BytesIO(raw)

    captured: dict = {}

    def start_response(
        status: str,
        headers: list[tuple[str, str]],
    ) -> None:
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = b"".join(app(environ, start_response))
    code = int(captured["status"].split()[0])
    content_type = captured["headers"].get("Content-Type", "")

    if content_type.startswith("application/json"):
        return code, json.loads(body.decode("utf-8"))

    return code, body.decode("utf-8")
