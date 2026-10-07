import csv
from pathlib import Path
rows = list(csv.DictReader(Path('.experiment/decisions.tsv').open(), delimiter='\t'))
start = next(i for i, row in enumerate(rows) if row['decision'] == 'Fresh serial helper owns tests and four application files')
for row in rows[start:]:
    for evidence in row['evidence'].split('; '):
        assert Path(evidence).is_file(), evidence
    print(row['phase'], row['decision'], row['result'], sep=' | ')
report = Path('.experiment/helper-implementation-report.md').read_text()
assert 'b04219d12bf6e1d60782a75e354bac273a7168bd' in report
for label in ['pause-focused-before', 'pause-route-boundary-before', 'pause-focused-final', 'pause-full-public-final', 'pause-final-diff-check']:
    path = Path('.experiment') / (label + '.log')
    assert path.is_file(), path
print('Helper decision evidence resolves; final test, diff and commit artifacts present. Raw transcript is not claimed.')
