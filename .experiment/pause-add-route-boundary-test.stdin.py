from pathlib import Path
path = Path('tests/test_pause.py')
source = path.read_text()
before = '            for path in (f"/api/jobs/daily-report/extra/{action}",\n'
after = '            for path in (f"api/jobs/daily-report/{action}",\n                         f"prefix/api/jobs/daily-report/{action}",\n                         f"/api/jobs/daily-report/extra/{action}",\n'
assert source.count(before) == 1
path.write_text(source.replace(before, after))
