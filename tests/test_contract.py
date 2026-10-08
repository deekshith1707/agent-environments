import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = ROOT / "environments"
REQUIRED_KEYS = {"id", "category", "title", "version", "timeout_seconds",
                 "task", "constraints", "reward", "artifacts"}


class ScenarioContractTests(unittest.TestCase):
    def test_every_environment_has_valid_scenario_metadata(self):
        paths = sorted(ENVIRONMENTS.glob("env_*/scenario.json"))
        self.assertEqual(len(paths), 5)
        for path in paths:
            with self.subTest(path=path):
                scenario = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED_KEYS <= scenario.keys())
                self.assertEqual(scenario["id"], path.parent.name)
                self.assertGreater(scenario["timeout_seconds"], 0)
                self.assertIsInstance(scenario["constraints"], list)
                self.assertEqual(scenario["reward"], {"pass": 1, "fail": 0})
                self.assertTrue(scenario["artifacts"])

    def test_scaffold_generates_contract_and_rejects_bad_id(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scaffold.py"), "--id", "006",
                 "--name", "cron_job_setup", "--category", "system_admin"],
                cwd=directory, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            scenario_path = Path(directory) / "environments/env_006_cron_job_setup/scenario.json"
            self.assertEqual(json.loads(scenario_path.read_text())["id"], "env_006_cron_job_setup")

            bad = subprocess.run(
                [sys.executable, str(ROOT / "scaffold.py"), "--id", "6",
                 "--name", "bad", "--category", "system_admin"],
                cwd=directory, capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(bad.returncode, 0)


if __name__ == "__main__":
    unittest.main()
