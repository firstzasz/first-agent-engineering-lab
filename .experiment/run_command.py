import json
import subprocess
import sys
from pathlib import Path

output_path = Path(sys.argv[1])
command = sys.argv[2:]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
output_path.write_text(result.stdout)
with Path('.experiment/actions.jsonl').open('a') as log:
    log.write(json.dumps({'kind': 'command', 'argv': command, 'cwd': str(Path.cwd()), 'exit_code': result.returncode, 'output_path': str(output_path)}) + '\n')
print(result.stdout, end='')
sys.exit(result.returncode)
