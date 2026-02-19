#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HASH_PATTERN = re.compile(
    r"^APPROVAL_HASH: [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}-\d+-APPROVED$",
    re.MULTILINE,
)


def get_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    return Path.cwd().resolve()


def resolve_markdown_file(path_value: str, repo_root: Path) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve(strict=False)

    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"Path is outside repository root: {path}") from exc

    if path.suffix.lower() != ".md":
        raise ValueError(f"Only .md files are allowed: {path}")

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    return path


def verify_gate(backlog_path: Path) -> tuple[bool, str]:
    content = backlog_path.read_text(encoding="utf-8")
    matches = HASH_PATTERN.findall(content)

    if not matches:
        return (
            False,
            "No valid APPROVAL_HASH found. Expected format: APPROVAL_HASH: <UUID>-<TIMESTAMP>-APPROVED",
        )

    return True, matches[0]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify that backlog file contains valid APPROVAL_HASH entry.",
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to APPROVED_BACKLOG.md (must be inside repository).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = get_repo_root()

    try:
        backlog_path = resolve_markdown_file(args.file, repo_root)
        ok, details = verify_gate(backlog_path)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if not ok:
        print(f"FAIL: {details}")
        return 1

    print(f"SUCCESS: Found valid hash: {details}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
