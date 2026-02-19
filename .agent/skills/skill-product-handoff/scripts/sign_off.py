#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
import time
import uuid
from pathlib import Path


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


def resolve_markdown_file(path_value: str, repo_root: Path, must_exist: bool = True) -> Path:
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

    if must_exist and not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    return path


def sign_off(backlog_path: Path) -> str:
    unique_id = uuid.uuid4()
    timestamp = int(time.time())
    hash_line = f"APPROVAL_HASH: {unique_id}-{timestamp}-APPROVED"

    with backlog_path.open("a", encoding="utf-8") as file_handle:
        file_handle.write("\n" + hash_line + "\n")

    return hash_line


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Append APPROVAL_HASH to an approved backlog markdown file.",
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
        backlog_path = resolve_markdown_file(args.file, repo_root, must_exist=True)
        hash_line = sign_off(backlog_path)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"SUCCESS: Signed off on {backlog_path}")
    print(f"Hash: {hash_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
