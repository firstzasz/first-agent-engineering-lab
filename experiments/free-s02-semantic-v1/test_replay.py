"""Local, no-key selftests for V1 semantic evidence replay.

Tests validate anchor provenance/contract and adversarial gold fixture structure.
They do NOT assert that a regex can understand natural-language semantics.
"""
import json
import unittest
from pathlib import Path
from replay import judge_record, evaluate, CRITERIA

HERE=Path(__file__).resolve().parent

class TestV1Replay(unittest.TestCase):
    def test_explicit_anchor_passes(self):
        q=[{"question":"Should manual runs be allowed while a Job is paused?"}]
        label={"status":"EXPLICIT","index":1,
               "quote":"manual runs be allowed","rationale":"Specific manual start policy"}
        result=judge_record(label,q)
        self.assertEqual(result["credit"],1)
        self.assertEqual(len(result["question_sha256"]),64)

    def test_partial_never_credited(self):
        q=[{"question":"Does pause block only scheduled or manual runs?"}]
        result=judge_record({"status":"PARTIAL","index":1,
            "quote":"scheduled or manual runs","rationale":"No skipped scheduled trigger disposition"},q)
        self.assertEqual(result["credit"],0)

    def test_forged_quote_rejected(self):
        q=[{"question":"Does resume endpoint return 200?"}]
        with self.assertRaisesRegex(ValueError,"QUOTE_NOT_IN_FROZEN_QUESTION"):
            judge_record({"status":"EXPLICIT","index":1,
                "quote":"catch up missed scheduled runs",
                "rationale":"Unsupported claim about resume policy"},q)

    def test_wrong_index_rejected(self):
        q=[{"question":"What happens to a running Run when paused?"}]
        with self.assertRaisesRegex(ValueError,"INVALID_QUESTION_INDEX"):
            judge_record({"status":"EXPLICIT","index":2,
                "quote":"running Run when paused",
                "rationale":"Correct intent but wrong question index"},q)

    def test_absent_with_quote_rejected(self):
        q=[{"question":"Should a job have a paused flag?"}]
        with self.assertRaisesRegex(ValueError,"UNANCHORED_LABEL_HAS_QUOTE"):
            judge_record({"status":"ABSENT","index":1,"quote":"paused flag",
                "rationale":"No frozen behavior contrast"},q)

    def test_not_adjudicated_never_promoted(self):
        r=judge_record({"status":"NOT_ADJUDICATED",
            "rationale":"No second independent reviewer available"},[])
        self.assertIsNone(r["credit"])

    def test_full_annotation_schema(self):
        p=json.loads((HERE/"ANNOTATIONS_PROVISIONAL.json").read_text("utf-8"))
        self.assertEqual(set(p["criteria"]),CRITERIA)
        self.assertEqual(len(p["cases"]),8)
        self.assertFalse(p["authoritative"])
        self.assertEqual(p["reviewer_blinding"],"UNBLINDED_SINGLE_ANALYST")
        for run,labels in p["cases"].items():
            with self.subTest(run=run):
                self.assertEqual(set(labels),CRITERIA)
                for label in labels.values():
                    self.assertIn(label["status"],{"EXPLICIT","PARTIAL","ABSENT","NOT_ADJUDICATED"})
                    self.assertGreater(len(label["rationale"]),11)

    def test_adversarial_fixture_is_nontrivial_and_complete(self):
        p=json.loads((HERE/"ADVERSARIAL_CASES.json").read_text("utf-8"))
        cases=p["cases"]
        self.assertGreaterEqual(len(cases),20)
        self.assertEqual(len({c["id"] for c in cases}),len(cases))
        observed=set()
        negatives=0
        compounds=0
        for c in cases:
            expected=c["expected_decision_ids"]
            self.assertEqual(len(expected),len(set(expected)))
            self.assertTrue(set(expected)<=CRITERIA)
            self.assertGreater(len(c["reason"]),8)
            self.assertGreater(len(c["question"]),20)
            observed.update(expected)
            negatives+=not bool(expected)
            compounds+=len(expected)>1
        self.assertEqual(observed,CRITERIA)
        self.assertGreaterEqual(negatives,5)
        self.assertGreaterEqual(compounds,2)

    def test_no_historical_score_overwrite(self):
        p=json.loads((HERE/"ANNOTATIONS_PROVISIONAL.json").read_text("utf-8"))
        self.assertNotIn("original_frozen_matcher_score",p)
        self.assertEqual(p["source_run"],41222993755)

if __name__=="__main__":
    unittest.main()
