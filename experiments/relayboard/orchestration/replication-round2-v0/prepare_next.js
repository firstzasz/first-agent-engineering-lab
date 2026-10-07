(async()=>{
const id=load("next_run_id"),run=load("procedural_runs").find(r=>r.run_id===id),repo=load("repo");
const r=await tools.exec_command({cmd:"python runtime.py prepare "+id,workdir:"/workspace/relayboard-round2-control",max_output_tokens:12000});if(r.exit_code!==0)throw Error(r.output);
const start=JSON.parse(r.output);store("active_start",start);store("active_run_id",id);store("operator_interactions",[]);
const q=load("active_queue");q.runs.find(x=>x.run_id===id).status="RUNNING";store("active_queue",q);
const f=await tools.mcp__codex_apps__github_create_file({repository_full_name:repo,branch:"research/batch-orchestration-round2",path:load("active_batch_root")+"/results/"+id+"/start.json",message:"research: record fresh serial "+id+" start",content:JSON.stringify({status:"RUNNING",...start},null,2)+"\n"});if(f.isError)throw Error(JSON.stringify(f));
const sha=f.structuredContent.commit_sha;const t=await tools.mcp__codex_apps__github_fetch({url:"https://api.github.com/repos/"+repo+"/git/commits/"+sha});if(t.isError)throw Error(JSON.stringify(t));store("research_head",sha);store("research_tree",JSON.parse(t.structuredContent.content).tree.sha);
text({id,start,record_commit:sha});
})()
