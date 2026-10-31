import unittest
from live import MODEL,MARKER,ROLES,MAX_REQUESTS,make_payload,source_safe
from grade_live import evaluate

class HostPreflightTests(unittest.TestCase):
    def test_each_role_fresh_exact_two_messages(self):
        payloads=[make_payload(r,"def normalize_tag(s):\n    return s.lower()") for r in ROLES]
        for role,p in zip(ROLES,payloads):
            self.assertEqual(p["model"],MODEL)
            self.assertEqual(len(p["messages"]),2)
            self.assertEqual(len(p["tools"]),1)
            self.assertEqual(p["tool_choice"],"auto")
            self.assertEqual(p["max_tokens"],320)
        self.assertEqual([MARKER in str(p) for p in payloads],[True,False,False])
        self.assertNotEqual(payloads[0]["messages"],payloads[1]["messages"])

    def test_safe_source_syntax_and_restrictions(self):
        self.assertTrue(source_safe("def normalize_tag(s):\n    return s.lower()")[0])
        self.assertFalse(source_safe("import os\ndef normalize_tag(s):\n    return os.getenv('KEY')")[0])
        self.assertFalse(source_safe("def other_function(s):\n    return s")[0])
        self.assertFalse(source_safe("def normalize_tag(s):\n    return open('/etc/passwd').read()")[0])

    def test_missing_role_results_cannot_pass(self):
        grader=evaluate({"experiment":"FREE_ULTRA_HELPER_SMOKE_V0",
                         "requested_model":MODEL,"rows":[]})
        self.assertFalse(grader["capability_verified"])
        self.assertFalse(grader["checks"]["three_sequential_roles"])

    def test_budget_and_model_fixed(self):
        self.assertEqual(MAX_REQUESTS,3)
        self.assertEqual(MODEL,"nvidia/nemotron-3-ultra-550b-a55b")
        for r in ROLES:
            self.assertNotIn("deepseek",str(make_payload(r,"")))

if __name__=="__main__":
    unittest.main()
