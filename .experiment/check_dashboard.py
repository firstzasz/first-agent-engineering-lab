from relayboard.testing import request
from relayboard.web import create_seeded_app

status, body = request(create_seeded_app(), "GET", "/dashboard")
assert status == 200, status
assert "<th>Latest result</th>" in body, body
assert "<th>Last result</th>" not in body, body
print("PASS: GET /dashboard displays Latest result and omits Last result")
