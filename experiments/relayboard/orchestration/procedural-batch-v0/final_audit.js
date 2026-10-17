(async()=>{
const repo=load("repo"),expected=load("research_head"),prefix="https://api.github.com/repos/"+repo;
const requests=[["repository",prefix],["branch",prefix+"/branches/research/batch-orchestration-pilot"],["ref",prefix+"/git/ref/heads/research/batch-orchestration-pilot"],["tree",prefix+"/git/trees/"+expected+"?recursive=1"],["main",prefix+"/git/ref/heads/main"],["N01branch",prefix+"/git/ref/heads/treatment/neutral/N-S01-001"],...load("active_queue").runs.map(r=>["PR:"+r.run_id,prefix+"/pulls/"+load("candidate_pr:"+r.run_id).number]),...load("active_queue").runs.map(r=>["candidate:"+r.run_id,prefix+"/git/ref/heads/candidate/"+r.run_id])];
const rs=await Promise.allSettled(requests.map(async([key,url])=>{const r=await tools.mcp__codex_apps__github_fetch({url});if(r.isError)throw Error(JSON.stringify(r));return [key,JSON.parse(r.structuredContent.content)];}));
const map=new Map(rs.map(r=>{if(r.status!=="fulfilled")throw r.reason;return r.value;}));
if(map.get("repository").full_name!==repo)throw Error("repo mismatch");
if(map.get("branch").name!=="research/batch-orchestration-pilot"||map.get("branch").commit.sha!==expected||map.get("ref").object.sha!==expected)throw Error("research branch/ref/expected head mismatch");
if(map.get("tree").truncated)throw Error("tree truncated");
const treeMap=new Map(map.get("tree").tree.map(f=>[f.path,f.sha]));
const fixture=load("lab_tree").tree.filter(f=>f.type==="blob"&&f.path.startsWith("fixtures/relayboard/")).map(({path,sha})=>({path,sha}));
const frozen=[...load("frozen_audit_baseline"),...load("port_frozen_blob_baseline"),...fixture,{path:"experiments/relayboard/runs/neutral/N-S01-001.json",sha:"f54d06d29f9f7880778b877300d341fdb6810f0a"}];
const drift=frozen.filter(f=>treeMap.get(f.path)!==f.sha);if(drift.length)throw Error("Frozen drift "+JSON.stringify(drift));
const checks=load("active_queue").runs.map(r=>{const pr=map.get("PR:"+r.run_id),ref=map.get("candidate:"+r.run_id),c=load("remote_candidate:"+r.run_id);if(pr.base.ref!==r.branch||pr.head.sha!==c.sha||ref.object.sha!==c.sha||pr.merged||!pr.draft)throw Error("Candidate/PR mismatch "+r.run_id);return {run_id:r.run_id,sha:c.sha,tree_sha:c.tree_sha,pr:pr.number,base:pr.base.ref,draft:pr.draft,merged:pr.merged};});
if(map.get("main").object.sha!=="d7d277c0e684d1e9aed0c30259796deb48c7c207")throw Error("Main changed since task start; inspect external cause.");
if(map.get("N01branch").object.sha!=="563952fab378eda87da696cda4df12fe5c9d4e5e")throw Error("N01 branch drift");
const audit={observed_at:(await tools.clock__curr_time({})).current_time,repository:repo,branch:map.get("branch").name,verified_research_head:expected,branch_and_remote_ref_match:true,main_head:map.get("main").object.sha,main_unchanged:true,N_S01_001:{record_blob:"f54d06d29f9f7880778b877300d341fdb6810f0a",treatment_head:map.get("N01branch").object.sha,unchanged:true,rerun:false},frozen_blob_checks:frozen,drift:[],candidate_pr_checks:checks,merge_performed:false,all_dispositions:load("active_queue").runs.map(({run_id,status})=>({run_id,status}))};
store("final_audit",audit);text({head:expected,frozen_blob_count:frozen.length,main_unchanged:true,N01_untouched:true,candidates:checks.length,merge_performed:false});})()
