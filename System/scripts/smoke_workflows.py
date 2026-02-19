#!/usr/bin/env python3
"""Smoke checks for workflow integrity."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEY_WORKFLOWS = [
    "base-stub-first.md",
    "vdd-enhanced.md",
    "light-01-start-feature.md",
    "light-02-develop-task.md",
]

# Intentionally validate explicit nested workflow calls only: "Call /workflow-name"
CALL_RE = re.compile(r"\b(?:Call|call)\s+`?/([a-z0-9-]+)`?")


def check_key_workflows(workflows_dir: Path) -> list[str]:
    errors: list[str] = []
    for wf_name in KEY_WORKFLOWS:
        wf_path = workflows_dir / wf_name
        if not wf_path.is_file():
            errors.append(f"Missing key workflow: .agent/workflows/{wf_name}")
    return errors


def check_internal_calls(workflows_dir: Path) -> list[str]:
    errors: list[str] = []

    for wf_path in sorted(workflows_dir.glob("*.md")):
        try:
            content = wf_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = wf_path.read_text(encoding="utf-8", errors="ignore")

        for line_num, line in enumerate(content.splitlines(), start=1):
            for match in CALL_RE.finditer(line):
                called = match.group(1)
                called_path = workflows_dir / f"{called}.md"
                if not called_path.is_file():
                    rel_wf = wf_path.as_posix().split("/.agent/")[-1]
                    errors.append(
                        f"{rel_wf}:{line_num}: missing called workflow -> .agent/workflows/{called}.md"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-check workflow files")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    workflows_dir = repo_root / ".agent/workflows"

    if not workflows_dir.is_dir():
        print("Missing .agent/workflows directory", file=sys.stderr)
        return 2

    errors = []
    errors.extend(check_key_workflows(workflows_dir))
    errors.extend(check_internal_calls(workflows_dir))

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        print(f"Workflow smoke checks failed with {len(errors)} issue(s).", file=sys.stderr)
        return 1

    print("Workflow smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
