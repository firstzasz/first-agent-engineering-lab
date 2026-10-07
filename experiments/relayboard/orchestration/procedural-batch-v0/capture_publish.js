(async()=>{
const id=load("active_run_id"),repo=load("repo"),run=load("procedural_runs").find(r=>r.run_id===id);
const result=await tools.exec_command({cmd:"python runtime.py capture "+id,workdir:"/workspace/relayboard-batch-control",max_output_tokens:4000});if(result.exit_code!==0)throw Error(result.output);text(result.output);
const sizeR=await tools.exec_command({cmd:"python - <<'PY'\nfrom pathlib import Path\nprint(len(Path('"+id+"-capture.json').read_text()))\nPY",workdir:"/workspace/relayboard-batch-control",max_output_tokens:1000});const size=Number(sizeR.output.trim()),pieces=[];
for(let offset=0;offset<size;offset+=18000)pieces.push({offset,cmd:"python - <<'PY'\nfrom pathlib import Path\nimport sys\nsys.stdout.write(Path('"+id+"-capture.json').read_text()["+offset+":"+Math.min(offset+18000,size)+"])\nPY"});
const chunks=await Promise.allSettled(pieces.map(async p=>{const r=await tools.exec_command({cmd:p.cmd,workdir:"/workspace/relayboard-batch-control",max_output_tokens:18000});if(r.exit_code!==0||r.output.startsWith("Warning:"))throw Error("Capture read failed");return {offset:p.offset,text:r.output};}));
const capture=JSON.parse(chunks.map(r=>{if(r.status==="rejected")throw r.reason;return r.value;}).sort((a,b)=>a.offset-b.offset).map(r=>r.text).join(""));
let accessReport=null;try{accessReport=JSON.parse(capture.files.find(f=>f.path===".experiment/REPORT.json"||f.path==="REPORT.json")?.content||"null");}catch{}
const accessKeys=["evaluator_or_peer_material_accessed","evaluator_material_accessed","peer_material_accessed","peer_or_control_material_accessed","hidden_reference_solution_accessed","oracle_reference_material_accessed","peer_other_run_material_accessed","deliberate_hidden_material_retrieval"];
if(accessReport?.contaminated===true||accessReport?.contamination===true||[accessReport,accessReport?.access_declaration,accessReport?.boundary].filter(Boolean).some(obj=>accessKeys.some(k=>obj[k]===true)))store("observed_contamination:"+id,true);
capture.local_commits=capture.local_commits.map(({patch,...meta})=>meta);store("capture:"+id,capture);
if(capture.immutable_packet_drift.length)notify({invalid_packet_drift:capture.immutable_packet_drift});
const tree=await tools.mcp__codex_apps__github_create_tree({repository_full_name:repo,tree_elements:capture.files});if(tree.isError)throw Error(JSON.stringify(tree));
if(tree.structuredContent.sha!==capture.local_candidate_tree)throw Error("Remote candidate tree differs");
const commit=await tools.mcp__codex_apps__github_create_commit({repository_full_name:repo,parent_sha:run.prepared_sha,tree_sha:tree.structuredContent.sha,message:"benchmark: freeze "+id+" "+run.treatment+" candidate (local "+capture.local_candidate_sha+")"});if(commit.isError)throw Error(JSON.stringify(commit));
const br=await tools.mcp__codex_apps__github_create_branch({repository_full_name:repo,branch_name:"candidate/"+id,sha:commit.structuredContent.sha});if(br.isError)throw Error(JSON.stringify(br));
store("remote_candidate:"+id,{sha:commit.structuredContent.sha,tree_sha:tree.structuredContent.sha,branch:"candidate/"+id});
const ref=await tools.mcp__codex_apps__github_fetch({url:"https://api.github.com/repos/"+repo+"/git/ref/heads/candidate/"+id});if(ref.isError||JSON.parse(ref.structuredContent.content).object.sha!==commit.structuredContent.sha)throw Error("Candidate ref readback mismatch");
const clean=await tools.exec_command({cmd:"python runtime.py clean "+id,workdir:"/workspace/relayboard-batch-control",max_output_tokens:1000});if(clean.exit_code!==0)throw Error(clean.output);
let ev;
if(load("observed_contamination:"+id)===true){
ev={schema_version:1,run_id:id,context:"Hidden evaluation not executed: contaminated candidate excluded; worker public evidence remains archived.",local_candidate_sha:capture.local_candidate_sha,candidate_tree:capture.local_candidate_tree,public_tests:{passed:null,skipped:true,reason:"No post-termination public rerun; see frozen worker logs."},oracle:{scenario:run.scenario,passed:null,failures:[],error:null,skipped:true,reason:"CONTAMINATED before freeze; excluded without hidden evaluation."},feedback_to_contestant:false};
store("evaluation:"+id,ev);
}else{
const exactSource=load("frozen_evaluator").content.replace(/\n$/,"");
await tools.apply_patch("*** Begin Patch\n*** Add File: /workspace/relayboard-batch-control/evaluator-active/evaluator.py\n"+exactSource.split("\n").map(l=>"+"+l).join("\n")+"\n*** End Patch");
const evaluation=await tools.exec_command({cmd:"python evaluate_frozen.py "+id,workdir:"/workspace/relayboard-batch-control",max_output_tokens:15000});if(evaluation.exit_code!==0)throw Error(evaluation.output);
ev=JSON.parse(evaluation.output);if(ev.evaluator_blob_sha!=="3aaaa9924f09ba18a5888d94373a9edc04187926")throw Error("Evaluator source drift");store("evaluation:"+id,ev);
await tools.exec_command({cmd:"python - <<'PY'\nimport shutil\nshutil.rmtree('evaluator-active')\nPY",workdir:"/workspace/relayboard-batch-control",max_output_tokens:1000});
}
const bundleMeta=await tools.exec_command({cmd:"python - <<'PY'\nfrom pathlib import Path\nimport hashlib,base64,json\nb=Path('"+id+"-candidate.bundle').read_bytes()\npayload=json.dumps({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'base64':base64.b64encode(b).decode()})\nPath('"+id+"-bundle.json').write_text(payload)\nprint(len(payload))\nPY",workdir:"/workspace/relayboard-batch-control",max_output_tokens:1000});if(bundleMeta.exit_code!==0)throw Error(bundleMeta.output);
const bundleSize=Number(bundleMeta.output.trim()),bundleChunks=await Promise.allSettled(Array.from({length:Math.ceil(bundleSize/18000)},(_,i)=>tools.exec_command({cmd:"python - <<'PY'\nfrom pathlib import Path\nimport sys\nsys.stdout.write(Path('"+id+"-bundle.json').read_text()["+i*18000+":"+Math.min((i+1)*18000,bundleSize)+"])\nPY",workdir:"/workspace/relayboard-batch-control",max_output_tokens:18000})));
store("bundle:"+id,JSON.parse(bundleChunks.map(r=>{if(r.status!=="fulfilled"||r.value.exit_code!==0||r.value.output.startsWith("Warning:"))throw Error("Bundle chunk read failed");return r.value.output;}).join("")));
const pr=await tools.mcp__codex_apps__github_create_pull_request({repository_full_name:repo,head:"candidate/"+id,base:run.branch,draft:true,title:id+": "+run.treatment+" frozen benchmark candidate",body:"Implements the frozen "+run.scenario+" task in a fresh "+run.treatment+" context from Pilot Start State v0.1. Local history and separate post-termination evaluation evidence are retained on research/batch-orchestration-pilot. This benchmark PR targets only its treatment branch and must not be merged into main."});if(pr.isError)throw Error(JSON.stringify(pr));store("candidate_pr:"+id,pr.structuredContent);
text({frozen_candidate:id,remote_sha:commit.structuredContent.sha,public_pass:ev.public_tests.passed,hidden_pass:ev.oracle.passed,pr:pr.structuredContent.url});
await eval(load("finalize_script"));
})()
