from __future__ import annotations
import argparse,datetime,hashlib,json,os,shutil,subprocess
from pathlib import Path
CONTROL=Path('/workspace/relayboard-batch-control')
ACTIVE=Path('/workspace/relayboard-active')
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load_runs(): return json.loads((CONTROL/'delivery.json').read_text())['runs']
def git(root,*args):
 p=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr)
 return p.stdout
def blob(text):
 b=text.encode();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def prepare(run_id):
 r=next(r for r in load_runs() if r['run_id']==run_id)
 root=ACTIVE/run_id
 ACTIVE.mkdir(exist_ok=True)
 assert not any(ACTIVE.iterdir()),'A peer working area is still active'
 assert not Path('/tmp/batch-orchestration-preflight').exists()
 assert not Path('/workspace/relayboard-procedural-pilot').exists()
 assert not Path('/workspace/relayboard-batch-control/evaluator-active').exists(),'Evaluator must be removed before contestant delivery'
 root.mkdir()
 for name,content in r['files'].items():
  p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
 git(root,'init','-b','candidate/'+run_id)
 git(root,'config','user.name','RelayBoard Pilot')
 git(root,'config','user.email','benchmark@example.invalid')
 git(root,'add','.')
 git(root,'commit','-m','benchmark: frozen standalone '+run_id+' starting packet')
 start=git(root,'rev-parse','HEAD').strip();tree=git(root,'rev-parse','HEAD^{tree}').strip()
 assert tree==r['prepared_tree_sha'],'Local packet differs from verified remote preparation tree'
 files={name:blob(content) for name,content in r['files'].items()}
 assert not any('evaluator/' in name or 'ORACLE' in name or 'reference_solution' in name for name in files)
 record={'run_id':run_id,'workspace':str(root),'local_start_sha':start,'local_start_tree':tree,'remote_prepared_sha':r['prepared_sha'],'base_sha':r['base_sha'] if 'base_sha' in r else json.loads(r['files']['.experiment/RUN_MANIFEST.json'])['base_sha'],'treatment':r['treatment'],'prepared_at':stamp(),'files':files,'no_lab_remote':git(root,'remote','-v')=='','independent_history':len(git(root,'rev-list','--all').splitlines())==1}
 (CONTROL/(run_id+'-start.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record))
def capture(run_id):
 r=next(r for r in load_runs() if r['run_id']==run_id);root=ACTIVE/run_id
 start=json.loads((CONTROL/(run_id+'-start.json')).read_text())
 git(root,'add','-A')
 dirty=git(root,'diff','--cached','--name-only').strip()
 if dirty:git(root,'commit','-m','benchmark: orchestrator freezes remaining contestant artifacts for '+run_id)
 final=git(root,'rev-parse','HEAD').strip()
 files=[]
 for path in git(root,'ls-files','-z').split('\0'):
  if not path:continue
  p=root/path
  assert not p.is_symlink(),'Candidate symlink not supported'
  files.append({'path':path,'mode':'100755' if os.stat(p).st_mode & 0o111 else '100644','type':'blob','content':p.read_text()})
 immutable=[name for name in r['files'] if name=='TASK.md' or name=='METHOD.md' or name.startswith('upstream/') or name=='.experiment/RUN_MANIFEST.json']
 drift=[name for name in immutable if not (root/name).is_file() or (root/name).read_text()!=r['files'][name]]
 history=[]
 for sha in reversed(git(root,'rev-list','HEAD').splitlines()):
  history.append({'sha':sha,'metadata':git(root,'show','-s','--format=fuller',sha),'patch':git(root,'show','--format=','--binary',sha)})
 capture={'run_id':run_id,'start':start,'frozen_at':stamp(),'local_candidate_sha':final,'local_candidate_tree':git(root,'rev-parse','HEAD^{tree}').strip(),'local_commits':history,'diff':git(root,'diff','--binary',start['local_start_sha'],final),'diff_stat':git(root,'diff','--stat',start['local_start_sha'],final),'files':files,'immutable_packet_drift':drift,'remote_list':git(root,'remote','-v'),'status':git(root,'status','--short')}
 (CONTROL/(run_id+'-capture.json')).write_text(json.dumps(capture)+'\n')
 snapshot=CONTROL/'snapshots'/run_id;snapshot.mkdir(parents=True)
 for f in files:
  p=snapshot/f['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f['content'])
 (CONTROL/(run_id+'-candidate.bundle')).parent.mkdir(exist_ok=True)
 git(root,'bundle','create',str(CONTROL/(run_id+'-candidate.bundle')),'--all')
 print(json.dumps({'run_id':run_id,'local_candidate_sha':final,'local_candidate_tree':capture['local_candidate_tree'],'immutable_packet_drift':drift,'files':len(files),'commits':len(history),'diff_stat':capture['diff_stat'],'snapshot':str(snapshot),'frozen_at':capture['frozen_at']}))
def clean(run_id):
 root=ACTIVE/run_id
 assert (CONTROL/(run_id+'-capture.json')).is_file(),'Capture evidence first'
 shutil.rmtree(root)
 eval_root=CONTROL/'evaluator-active'
 if eval_root.exists():shutil.rmtree(eval_root)
 print(json.dumps({'run_id':run_id,'contestant_area_removed':not root.exists(),'evaluator_area_removed':not eval_root.exists()}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','capture','clean']);p.add_argument('run_id');a=p.parse_args()
 {'prepare':prepare,'capture':capture,'clean':clean}[a.command](a.run_id)
