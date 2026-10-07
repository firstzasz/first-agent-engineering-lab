"""Compare public WSGI responses before and after the heading edit."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from relayboard.testing import request
from relayboard.web import create_seeded_app

root = Path(__file__).resolve().parent
app = create_seeded_app()
responses = {
    path: request(app, "GET", path)
    for path in ("/dashboard", "/api/jobs", "/api/alerts")
}
if sys.argv[1] == "baseline":
    assert responses["/dashboard"][0] == 200
    assert "<th>Last result</th>" in responses["/dashboard"][1]
    (root / "baseline-responses.json").write_text(json.dumps(responses, indent=2) + "\n")
    print("BASELINE: dashboard returns 200 and Jobs heading is Last result.")
elif sys.argv[1] == "verify":
    baseline = json.loads((root / "baseline-responses.json").read_text())
    expected_html = baseline["/dashboard"][1].replace(
        "<th>Last result</th>", "<th>Latest result</th>"
    )
    assert responses["/dashboard"][0] == 200
    assert responses["/dashboard"][1] == expected_html
    assert "<th>Latest result</th>" in responses["/dashboard"][1]
    assert "<th>Last result</th>" not in responses["/dashboard"][1]
    for path in ("/api/jobs", "/api/alerts"):
        assert list(responses[path]) == baseline[path], path
    (root / "verified-responses.json").write_text(json.dumps(responses, indent=2) + "\n")
    (root / "dashboard.html").write_text(responses["/dashboard"][1] + "\n")
    print("VERIFIED: GET /dashboard differs only by the requested heading; status 200.")
    print("VERIFIED: GET /api/jobs and GET /api/alerts match baseline responses.")
else:
    raise SystemExit("Choose baseline or verify")
