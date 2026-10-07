import sqlite3
from relayboard.store import Store
from relayboard.web import RelayBoardApp
from relayboard.testing import request
connection = sqlite3.connect(':memory:')
connection.executescript('''
CREATE TABLE jobs(id TEXT PRIMARY KEY, name TEXT NOT NULL, enabled INTEGER NOT NULL, max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1));
CREATE TABLE runs(id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs(id), source TEXT NOT NULL CHECK(source IN ('manual', 'scheduled')), status TEXT NOT NULL CHECK(status IN ('running', 'succeeded', 'failed')));
CREATE TABLE attempts(run_id TEXT NOT NULL REFERENCES runs(id), number INTEGER NOT NULL, succeeded INTEGER NOT NULL, PRIMARY KEY(run_id, number));
CREATE TABLE alerts(id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL REFERENCES runs(id), job_id TEXT NOT NULL REFERENCES jobs(id), kind TEXT NOT NULL, message TEXT NOT NULL);
INSERT INTO jobs VALUES('old', 'Old', 1, 2);
INSERT INTO runs VALUES('run-001', 'old', 'scheduled', 'failed');
INSERT INTO attempts VALUES('run-001', 1, 0);
INSERT INTO attempts VALUES('run-001', 2, 0);
INSERT INTO alerts VALUES(9, 'run-001', 'old', 'run_failed', 'Existing alert');
''')
before = {table: connection.execute('SELECT * FROM '+table).fetchall() for table in ('runs', 'attempts', 'alerts')}
app = RelayBoardApp(Store(connection))
expected = {'id':'old','name':'Old','enabled':True,'max_attempts':2,'paused':False}
assert request(app, 'GET', '/api/jobs') == (200, {'jobs':[expected]})
after = {table: [tuple(row) for row in connection.execute('SELECT * FROM '+table).fetchall()] for table in before}
assert after == before, (before, after)
assert request(app, 'POST', '/api/jobs/old/pause') == (200, {'job':dict(expected, paused=True)})
app = RelayBoardApp(Store(connection))
assert request(app, 'POST', '/api/jobs/old/runs', {'source':'scheduled'}) == (409, {'error':'job old is paused'})
assert '<td>failed</td><td>yes</td>' in request(app, 'GET', '/dashboard')[1]
assert request(app, 'GET', '/api/alerts') == (200, {'alerts':[{'id':9, 'run_id':'run-001', 'job_id':'old', 'kind':'run_failed', 'message':'Existing alert'}]})
assert request(app, 'POST', '/api/jobs/old/resume') == (200, {'job':expected})
assert request(app, 'POST', '/api/jobs/old/runs', {'source':'scheduled'}) == (201, {'run':{'id':'run-002', 'job_id':'old', 'source':'scheduled', 'status':'running'}})
print('PASS legacy schema migration preserves genuinely preexisting Run, Attempt and Alert rows and dashboard history; pause and reopen block scheduling; resume allows scheduling.')
connection.close()
