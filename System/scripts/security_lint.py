#!/usr/bin/env python3
"""Static security lint checks for core tool-runner guarantees."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

FORBIDDEN_PATTERNS = [
    ("System/scripts/tool_runner.py", "shell=True"),
    ("System/scripts/tool_runner.py", "startswith(str(repo_root))"),
]

REQUIRED_PATTERNS = [
    ("System/scripts/tool_runner.py", "relative_to(repo_root)"),
    ("System/scripts/tool_runner.py", "DISALLOWED_SHELL_CHARS"),
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    parser = argparse.ArgumentParser(description="Security lint for critical tool-runner patterns")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    failures = 0

    for rel, pattern in FORBIDDEN_PATTERNS:
        path = repo_root / rel
        if not path.is_file():
            print(f"FAIL: missing file {rel}")
            failures += 1
            continue

        content = _read_text(path)
        if pattern in content:
            print(f"FAIL: forbidden pattern '{pattern}' found in {rel}")
            failures += 1
        else:
            print(f"OK: forbidden pattern absent ({pattern})")

    for rel, pattern in REQUIRED_PATTERNS:
        path = repo_root / rel
        if not path.is_file():
            print(f"FAIL: missing file {rel}")
            failures += 1
            continue

        content = _read_text(path)
        if pattern not in content:
            print(f"FAIL: required pattern '{pattern}' missing in {rel}")
            failures += 1
        else:
            print(f"OK: required pattern present ({pattern})")

    if failures:
        print(f"Security lint failed with {failures} issue(s).", file=sys.stderr)
        return 1

    print("Security lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
