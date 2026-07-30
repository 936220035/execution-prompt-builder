from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "execution-prompt-builder" / "scripts" / "search_method_index.py"
INDEX = ROOT / "execution-prompt-builder" / "references" / "method-index.json"
sys.path.insert(0, str(SCRIPT.parent))
import search_method_index  # noqa: E402


class MethodRoutingTests(unittest.TestCase):
    def run_router(self, query: str, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), query, *extra], text=True, capture_output=True, check=False
        )

    def test_chinese_user_interview_matches_research(self) -> None:
        result = self.run_router("为新功能准备用户访谈和需求调研")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("user-research", result.stdout)

    def test_english_prd_and_acceptance_matches_specification(self) -> None:
        result = self.run_router("Write a PRD with user stories and acceptance criteria for an MVP")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("product-spec", result.stdout)

    def test_selection_never_exceeds_three_methods(self) -> None:
        result = self.run_router(
            "Define the user problem, run interviews, write a PRD, prioritize the roadmap, set pricing, analyze retention, research competitors, align stakeholders, and plan multi-agent handoff."
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(len([line for line in result.stdout.splitlines() if line and line[0].isdigit()]), 3)

    def test_operational_categories_are_gated(self) -> None:
        for query in (
            "线上数据库迁移报错，先排查故障",
            "Deploy the new version to production with rollback",
            "账号权限无法登录，请恢复访问",
        ):
            with self.subTest(query=query):
                result = self.run_router(query)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("METHOD_GATE category=non_product", result.stdout)

    def test_empty_input_is_rejected(self) -> None:
        result = self.run_router("   ")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Query must not be empty", result.stderr)

    def test_duplicate_identifiers_are_rejected(self) -> None:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        data["methods"].append(dict(data["methods"][0]))
        with tempfile.TemporaryDirectory() as temp_dir:
            duplicate_index = Path(temp_dir) / "methods.json"
            duplicate_index.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_router("用户访谈", "--index", str(duplicate_index))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Duplicate method id", result.stderr)


if __name__ == "__main__":
    unittest.main()
