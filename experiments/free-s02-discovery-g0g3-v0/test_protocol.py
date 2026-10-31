"""No-key deterministic preflight for frozen question/operator protocol."""
import unittest
from policy import classify, respond, FROZEN_ANSWERS
from runner import frozen_task, show, BASE, METHOD_SHA, METHOD_PATH

class FrozenDiscoveryProtocolTests(unittest.TestCase):
    def test_source_available(self):
        t=frozen_task()
        self.assertIn("pause",t.lower())
        self.assertIn("resume",t.lower())
        for path in METHOD_PATH.values():
            text=show(METHOD_SHA,path)
            self.assertIn("operator",text.lower())
        self.assertIn("class Store",show(BASE,"fixtures/relayboard/relayboard/store.py"))

    def test_exact_four_topics(self):
        self.assertEqual(len(FROZEN_ANSWERS),4)
        examples=[
            ("What happens to an already running Run when its Job is paused?",
             ["pause_in_progress_run"]),
            ("Should scheduled starts be skipped while a Job is paused?",
             ["scheduled_start_while_paused"]),
            ("Should a manual run start be allowed while the Job is paused?",
             ["manual_run_while_paused"]),
            ("On resume, should we catch up missed schedules or only future ones?",
             ["resume_behavior"]),
        ]
        for question,want in examples:
            with self.subTest(question=question):
                self.assertEqual(classify(question),want)

    def test_unrelated_fact_and_reversible_questions_not_credited(self):
        for q in [
            "Which module implements the schedule?",
            "What variable name should the database flag use?",
            "Does the user want a migration helper?",
            "Should we update the table schema?",
            "What are the four decisions?",
            "How do retries work in this code?",
        ]:
            with self.subTest(question=q):
                self.assertEqual(classify(q),[])

    def test_grouped_question_returns_only_explicit_policy(self):
        result, records=respond([
            "Should manual Run starts be allowed while Job is paused?",
            "Which file stores the scheduler state?",
        ])
        self.assertTrue(result["ok"])
        self.assertEqual(records[0]["matched"],["manual_run_while_paused"])
        self.assertEqual(records[1]["matched"],[])
        self.assertEqual(result["responses"][1]["answers"],[])
        self.assertNotIn("resume_behavior",str(result))

    def test_invalid_question_payload_fails(self):
        r,e=respond(["question"]*9)
        self.assertFalse(r["ok"])
        self.assertEqual(e,[])

if __name__=="__main__":
    unittest.main()
