import json
import shutil
import unittest
from pathlib import Path

from System.scripts.tool_runner import execute_tool


class TestToolRunner(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/temp_tool_test")
        self.test_dir.mkdir(exist_ok=True)
        (self.test_dir / "test.txt").write_text("hello world")
        self.repo_root = Path.cwd().resolve()

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_read_file_success(self):
        tool_call = {
            "name": "read_file",
            "arguments": json.dumps({"path": "tests/temp_tool_test/test.txt"}),
        }
        result = execute_tool(tool_call)
        self.assertTrue(result["success"])
        self.assertEqual(result["content"], "hello world")

    def test_read_file_not_found(self):
        tool_call = {
            "name": "read_file",
            "arguments": json.dumps({"path": "tests/temp_tool_test/missing.txt"}),
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"])

    def test_path_traversal(self):
        tool_call = {
            "name": "read_file",
            "arguments": json.dumps({"path": "../../../etc/passwd"}),
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("Path traversal", result["error"])

    def test_absolute_prefix_bypass_is_blocked(self):
        fake_path = f"{self.repo_root}-evil/test.txt"
        tool_call = {
            "name": "read_file",
            "arguments": json.dumps({"path": fake_path}),
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("Path traversal", result["error"])

    def test_write_file(self):
        tool_call = {
            "name": "write_file",
            "arguments": json.dumps({
                "path": "tests/temp_tool_test/new.txt",
                "content": "new content",
            }),
        }
        result = execute_tool(tool_call)
        self.assertTrue(result["success"])
        self.assertTrue((Path("tests/temp_tool_test/new.txt")).exists())

    def test_list_directory(self):
        tool_call = {
            "name": "list_directory",
            "arguments": {"path": "tests/temp_tool_test"},
        }
        result = execute_tool(tool_call)
        self.assertTrue(result["success"])
        self.assertIn("tests/temp_tool_test/test.txt", result["files"])

    def test_unknown_tool(self):
        tool_call = {"name": "fake_tool", "arguments": {}}
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("Unknown tool", result["error"])

    def test_run_tests_blocked_command(self):
        tool_call = {
            "name": "run_tests",
            "arguments": {"command": "rm -rf /"},
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("Command not allowed", result["error"])

    def test_run_tests_blocks_shell_metacharacters(self):
        tool_call = {
            "name": "run_tests",
            "arguments": {"command": "pytest -q; echo injected"},
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("metacharacters", result["error"])

    def test_run_tests_invalid_cwd_is_blocked(self):
        tool_call = {
            "name": "run_tests",
            "arguments": {"command": "pytest -q", "cwd": "../../../"},
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("Invalid working directory", result["error"])

    def test_run_tests_invalid_timeout(self):
        tool_call = {
            "name": "run_tests",
            "arguments": {"command": "pytest -q", "timeout_seconds": 0},
        }
        result = execute_tool(tool_call)
        self.assertFalse(result["success"])
        self.assertIn("timeout_seconds", result["error"])


if __name__ == "__main__":
    unittest.main()
