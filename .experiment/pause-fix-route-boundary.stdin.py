from pathlib import Path
path = Path('relayboard/web.py')
source = path.read_text()
before = '                and path_parts[1:3] == ["api", "jobs"]\n'
after = '                and path_parts[:3] == ["", "api", "jobs"]\n'
assert source.count(before) == 1
path.write_text(source.replace(before, after))
