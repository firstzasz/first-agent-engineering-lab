import json
import sys
from pathlib import Path

from relayboard.testing import request
from relayboard.web import create_seeded_app

baseline_path = Path('.experiment/baseline.json')
app = create_seeded_app()
code, dashboard = request(app, 'GET', '/dashboard')
api_code, api_jobs = request(app, 'GET', '/api/jobs')
assert code == 200, code
assert api_code == 200, api_code
if sys.argv[1:] == ['baseline']:
    assert '<th>Last result</th>' in dashboard
    assert '<th>Latest result</th>' not in dashboard
    baseline_path.write_text(json.dumps({'dashboard': dashboard, 'api_jobs': api_jobs}, indent=2) + '\n')
    print('PASS baseline GET /dashboard has Jobs table with Last result.')
    print('PASS baseline GET /api/jobs captured.')
else:
    baseline = json.loads(baseline_path.read_text())
    assert '<th>Latest result</th>' in dashboard, 'Latest result heading missing'
    assert '<th>Last result</th>' not in dashboard, 'Old heading still present'
    assert dashboard == baseline['dashboard'].replace('<th>Last result</th>', '<th>Latest result</th>'), 'Unrelated dashboard output changed'
    assert api_jobs == baseline['api_jobs'], 'GET /api/jobs changed'
    print('PASS GET /dashboard shows Latest result and differs only in that heading.')
    print('PASS GET /api/jobs equals baseline.')
