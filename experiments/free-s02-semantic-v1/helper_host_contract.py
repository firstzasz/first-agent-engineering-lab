"""Synthetic host-calibration contract for future pstack/Matt/FIRST comparisons.

No network, no model API and no executable untrusted agent code.
These checks prove *host boundary behavior*, not native method fidelity.
"""
from dataclasses import dataclass, field
import hashlib
from typing import Any

ALLOWED_FILES=frozenset({"TASK.md","GLOSSARY.md","relayboard/store.py",
                         "relayboard/service.py","relayboard/web.py","tests/test_public.py"})
WRITABLE_FILES=frozenset({"relayboard/store.py","relayboard/service.py","relayboard/web.py"})
ROLE_TOOLS={
    "lead":frozenset({"read_file","ask_operator","delegate","show_diff","run_public_tests"}),
    "implementer":frozenset({"read_file","write_file","run_public_tests","show_diff"}),
    "standards_reviewer":frozenset({"read_file","show_diff"}),
    "spec_reviewer":frozenset({"read_file","show_diff"}),
}
STAGES={
    "neutral":frozenset({"code_change","public_test","diff"}),
    "pstack":frozenset({"core_skill_read","playbook_read","implementer_delegated",
                        "public_test","independent_review","evidence_record"}),
    "matt":frozenset({"grill_with_docs","spec_or_narrow_route","implementer_delegated",
                      "public_test","standards_review","spec_review"}),
    "first":frozenset({"authority_classification","code_change",
                       "public_test","independent_verification","persistent_state"}),
}

class HostDenial(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code=code

@dataclass
class SharedBudget:
    max_requests:int
    max_tokens:int
    requests:int=0
    tokens:int=0
    def charge(self, request_tokens:int, completion_tokens:int)->None:
        if not all(isinstance(x,int) and x>=0 for x in (request_tokens,completion_tokens)):
            raise HostDenial("INVALID_USAGE")
        if self.requests+1>self.max_requests:
            raise HostDenial("REQUEST_CEILING")
        if self.tokens+request_tokens+completion_tokens>self.max_tokens:
            raise HostDenial("TOKEN_CEILING")
        self.requests+=1
        self.tokens+=request_tokens+completion_tokens

@dataclass
class ScopedSession:
    session_id:str
    role:str
    visible_files:dict[str,str]
    messages:list[dict[str,str]]=field(default_factory=list)
    actions:list[dict[str,Any]]=field(default_factory=list)
    def __post_init__(self):
        if self.role not in ROLE_TOOLS:
            raise HostDenial("UNKNOWN_ROLE")
        if not set(self.visible_files)<=ALLOWED_FILES:
            raise HostDenial("DISALLOWED_FILE_VISIBLE")
        if any("oracle" in k or "evaluator" in k for k in self.visible_files):
            raise HostDenial("ORACLE_LEAK")
    def invoke(self,tool:str,**kwargs):
        if tool not in ROLE_TOOLS[self.role]:
            raise HostDenial("ROLE_TOOL_DENIED")
        if tool=="read_file":
            path=kwargs.get("path")
            if path not in ALLOWED_FILES or path not in self.visible_files:
                raise HostDenial("READ_PATH_DENIED")
            result=self.visible_files[path]
        elif tool=="write_file":
            path=kwargs.get("path")
            source=kwargs.get("source")
            if path not in WRITABLE_FILES or path not in self.visible_files:
                raise HostDenial("WRITE_PATH_DENIED")
            if not isinstance(source,str) or len(source)>12000:
                raise HostDenial("INVALID_SOURCE_SIZE")
            # In this fake host, writes only modify its synthetic local snapshot.
            self.visible_files[path]=source
            result={"sha256":hashlib.sha256(source.encode()).hexdigest()}
        elif tool=="show_diff":
            result={"synthetic_diff_inspection":True}
        elif tool=="run_public_tests":
            result={"synthetic_host_only":True,"real_tests_executed":False}
        else:
            result={"synthetic_host_only":True}
        self.actions.append({"tool":tool,"path":kwargs.get("path"),"role":self.role})
        return result

class IsolatedHost:
    def __init__(self,synthetic_files:dict[str,str],budget:SharedBudget):
        if not set(synthetic_files)<=ALLOWED_FILES:
            raise HostDenial("BASE_FILE_DENIED")
        self._base=synthetic_files.copy()
        self.budget=budget
        self._serial=0
        self.sessions=[]
    def spawn(self,role:str,scope:tuple[str,...],instruction:str):
        if not set(scope)<=ALLOWED_FILES or not set(scope)<=self._base:
            raise HostDenial("SCOPE_DENIED")
        if not isinstance(instruction,str) or not instruction.strip():
            raise HostDenial("EMPTY_TASK")
        self._serial+=1
        s=ScopedSession(f"ctx-{self._serial:03d}",role,
            {name:self._base[name] for name in scope},
            messages=[{"role":"system","content":"synthetic restricted "+role},
                      {"role":"user","content":instruction}])
        self.sessions.append(s)
        return s
    def model_request(self,session:ScopedSession,prompt_tokens:int,completion_tokens:int):
        if session not in self.sessions:
            raise HostDenial("FOREIGN_CONTEXT")
        self.budget.charge(prompt_tokens,completion_tokens)
        # No real API request and no content/credential logs.
        session.actions.append({"model_request":True,"role":session.role,
                                "tokens":prompt_tokens+completion_tokens})
    def stage_coverage(self,method:str,observed_host_stages:set[str]):
        if method not in STAGES:
            raise HostDenial("UNKNOWN_METHOD")
        missing=sorted(STAGES[method]-observed_host_stages)
        return {"method":method,"required":sorted(STAGES[method]),
                "missing":missing,"fidelity_verified":not missing}
