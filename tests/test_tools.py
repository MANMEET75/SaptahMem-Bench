import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dev" / "episodes.jsonl"


def read_episodes():
    return [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


class ToolTests(unittest.TestCase):
    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / script)] + [str(arg) for arg in args], cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def test_current_fixture_passes_validation(self):
        result = self.run_script("validate_dataset.py", DATA)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validator_rejects_future_evidence(self):
        episodes = read_episodes()
        episodes[1]["questions"][0]["source_message_ids"] = ["e09"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "future.jsonl"
            write_jsonl(path, episodes)
            result = self.run_script("validate_dataset.py", path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not strictly before query cutoff", result.stderr)

    def test_scorer_accepts_variants_and_abstention(self):
        predictions = []
        for ep in read_episodes():
            for question in ep["questions"]:
                if question["answerability"] == "answerable":
                    answer = question.get("acceptable_answers", [question["gold_answer"]])[0]
                    abstained = False
                else:
                    answer = ""
                    abstained = True
                predictions.append({"episode_id": ep["episode_id"], "question_id": question["question_id"], "answer": answer, "abstained": abstained})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "predictions.jsonl"
            write_jsonl(path, predictions)
            result = self.run_script("score_predictions.py", "--gold", DATA, "--predictions", path, "--bootstrap", "50")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["summary"]["count"], 4)
        self.assertEqual(report["summary"]["category_macro_accuracy"], 1.0)

    def test_leakage_audit_runs_on_fixture(self):
        result = self.run_script("audit_leakage.py", DATA)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["episodes"], 2)


if __name__ == "__main__":
    unittest.main()
