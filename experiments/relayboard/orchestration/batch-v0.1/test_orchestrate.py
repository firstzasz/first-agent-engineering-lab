from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import orchestrate

ROOT = Path(__file__).resolve().parent

class Boundaries(unittest.TestCase):
    def test_packet_excludes_operator_oracle_and_peer_results(self):
        manifests = orchestrate.audit(ROOT)["manifests"]
        for m in manifests:
            text = json.dumps(orchestrate.packet(m))
            self.assertNotIn("S02_OPERATOR_ORACLE", text)
            self.assertNotIn("evaluation_path", text)
            self.assertNotIn("operator_interactions", text)
            for peer in manifests:
                if peer["run_id"] != m["run_id"]:
                    self.assertNotIn(peer["run_id"], text)

    def test_completed_run_cannot_enter_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "plan"
            shutil.copytree(ROOT, root)
            path = root / "batch.json"
            batch = json.loads(path.read_text())
            batch["runs"][0]["run_id"] = "N-S01-001"
            path.write_text(json.dumps(batch))
            with self.assertRaises(AssertionError):
                orchestrate.audit(root)

    def test_drifted_fixture_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "plan"
            shutil.copytree(ROOT, root)
            path = root / "runs/N-S02-001.json"
            m = json.loads(path.read_text())
            m["workspace"]["files"][0]["sha"] = "0" * 40
            path.write_text(json.dumps(m))
            with self.assertRaises(AssertionError):
                orchestrate.audit(root)

if __name__ == "__main__":
    unittest.main()
