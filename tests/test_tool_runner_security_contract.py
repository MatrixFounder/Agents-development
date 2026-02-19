from pathlib import Path


def test_tool_runner_no_shell_true_for_run_tests():
    src = Path("System/scripts/tool_runner.py").read_text(encoding="utf-8")
    assert "shell=True" not in src


def test_tool_runner_no_prefix_path_check():
    src = Path("System/scripts/tool_runner.py").read_text(encoding="utf-8")
    assert "startswith(str(repo_root))" not in src


def test_tool_runner_uses_relative_to_containment():
    src = Path("System/scripts/tool_runner.py").read_text(encoding="utf-8")
    assert "relative_to(repo_root)" in src


def test_tool_runner_has_shell_metachar_guard():
    src = Path("System/scripts/tool_runner.py").read_text(encoding="utf-8")
    assert "DISALLOWED_SHELL_CHARS" in src
