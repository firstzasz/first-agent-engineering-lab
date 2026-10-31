"""Pure offline helper-host security and fidelity-gate tests."""
import unittest
from helper_host_contract import (
    IsolatedHost, SharedBudget, HostDenial, STAGES
)

class HelperHostContractTests(unittest.TestCase):
    def setUp(self):
        self.host=IsolatedHost(
            {"TASK.md":"Synthetic task","relayboard/store.py":"original()",
             "relayboard/web.py":"web()","tests/test_public.py":"safe tests"},
            SharedBudget(max_requests=3,max_tokens=700),
        )

    def test_new_context_is_fresh_no_parent_messages(self):
        lead=self.host.spawn("lead",("TASK.md",),"Inspect task")
        lead.messages.append({"role":"assistant","content":"secret earlier reasoning"})
        worker=self.host.spawn("implementer",("relayboard/store.py",),"Implement isolated change")
        self.assertNotIn("secret earlier reasoning",str(worker.messages))
        self.assertNotIn("TASK.md",worker.visible_files)
        self.assertNotEqual(lead.session_id,worker.session_id)

    def test_reviewer_cannot_write(self):
        review=self.host.spawn("standards_reviewer",("relayboard/store.py",),"Review code without edits")
        with self.assertRaisesRegex(HostDenial,"ROLE_TOOL_DENIED"):
            review.invoke("write_file",path="relayboard/store.py",source="tamper()")
        self.assertEqual(review.invoke("read_file",path="relayboard/store.py"),"original()")

    def test_worker_write_local_snapshot_does_not_mutate_base(self):
        worker=self.host.spawn("implementer",("relayboard/store.py",),"Implement patch")
        worker.invoke("write_file",path="relayboard/store.py",source="patched()")
        other=self.host.spawn("spec_reviewer",("relayboard/store.py",),"Review baseline")
        self.assertEqual(other.invoke("read_file",path="relayboard/store.py"),"original()")
        self.assertEqual(worker.invoke("read_file",path="relayboard/store.py"),"patched()")

    def test_oracle_and_other_files_denied(self):
        lead=self.host.spawn("lead",("TASK.md",),"Inspect task")
        with self.assertRaisesRegex(HostDenial,"READ_PATH_DENIED"):
            lead.invoke("read_file",path="evaluator/oracle.py")
        with self.assertRaisesRegex(HostDenial,"SCOPE_DENIED"):
            self.host.spawn("lead",("evaluator/oracle.py",),"Access protected oracle")

    def test_shared_request_budget_includes_helpers_and_reviewers(self):
        a=self.host.spawn("lead",("TASK.md",),"Plan")
        b=self.host.spawn("implementer",("relayboard/store.py",),"Implement")
        c=self.host.spawn("spec_reviewer",("relayboard/store.py",),"Review")
        for s in (a,b,c):
            self.host.model_request(s,100,50)
        with self.assertRaisesRegex(HostDenial,"REQUEST_CEILING"):
            self.host.model_request(a,20,10)
        self.assertEqual(self.host.budget.requests,3)
        self.assertEqual(self.host.budget.tokens,450)

    def test_shared_token_budget_includes_helpers(self):
        a=self.host.spawn("lead",("TASK.md",),"Plan")
        b=self.host.spawn("implementer",("relayboard/store.py",),"Implement")
        self.host.model_request(a,300,100)
        with self.assertRaisesRegex(HostDenial,"TOKEN_CEILING"):
            self.host.model_request(b,200,150)
        self.assertEqual(self.host.budget.requests,1)

    def test_method_not_verified_by_document_only(self):
        for method in STAGES:
            with self.subTest(method=method):
                out=self.host.stage_coverage(method,set())
                self.assertFalse(out["fidelity_verified"])
                self.assertGreater(len(out["missing"]),0)
        # Explicitly represent a real host with every stage only as a capability
        # predicate test. This does not prove those stages happened in a model run.
        out=self.host.stage_coverage("matt",set(STAGES["matt"]))
        self.assertTrue(out["fidelity_verified"])

    def test_untrusted_tool_action_not_auto_promoted_to_evidence(self):
        w=self.host.spawn("implementer",("relayboard/store.py",),"Implement")
        fake=w.invoke("run_public_tests")
        self.assertFalse(fake["real_tests_executed"])
        self.assertTrue(fake["synthetic_host_only"])

    def test_empty_task_denied(self):
        with self.assertRaisesRegex(HostDenial,"EMPTY_TASK"):
            self.host.spawn("lead",("TASK.md",)," ")

if __name__=="__main__":
    unittest.main()
