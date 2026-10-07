import json
from pathlib import Path
import sys

from relayboard.testing import request
from relayboard.web import create_seeded_app

root = Path(__file__).resolve().parent
app = create_seeded_app()
code, body = request(app, 'GET', '/dashboard')
api_code, jobs = request(app, 'GET', '/api/jobs')
alerts_code, alerts = request(app, 'GET', '/api/alerts')
api = {'jobs_status': api_code, 'jobs': jobs, 'alerts_status': alerts_code, 'alerts': alerts}
mode = sys.argv[1]
(root / f'dashboard_{mode}.html').write_text(body)
(root / f'api_{mode}.json').write_text(json.dumps(api, sort_keys=True, indent=2) + '\n')
print(f'GET /dashboard status: {code}')
print(body)
assert code == 200
if mode == 'after':
    baseline = (root / 'dashboard_before.html').read_text()
    assert body == baseline.replace('<th>Last result</th>', '<th>Latest result</th>')
    assert api == json.loads((root / 'api_before.json').read_text())
    print('Dashboard equals baseline with only the requested heading replacement; GET jobs and alerts API payloads match baseline.')
assert '<th>Latest result</th>' in body, 'Requested Latest result heading is absent'
assert '<th>Last result</th>' not in body
print('Requested dashboard heading verified through WSGI.')
