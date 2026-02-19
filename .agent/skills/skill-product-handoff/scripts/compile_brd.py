#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
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


def resolve_markdown_read_path(path_value: str, repo_root: Path) -> Path:
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


def resolve_markdown_write_path(path_value: str, repo_root: Path) -> Path:
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

    if not path.parent.exists() or not path.parent.is_dir():
        raise FileNotFoundError(f"Output directory does not exist: {path.parent}")

    if path.exists() and path.is_dir():
        raise ValueError(f"Output path points to directory: {path}")

    return path


def compile_brd(
    market_strategy_path: Path,
    product_vision_path: Path,
    solution_blueprint_path: Path,
    output_path: Path,
    repo_root: Path,
) -> None:
    strategy_content = market_strategy_path.read_text(encoding="utf-8")
    vision_content = product_vision_path.read_text(encoding="utf-8")
    blueprint_content = solution_blueprint_path.read_text(encoding="utf-8")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rel_market = market_strategy_path.relative_to(repo_root)
    rel_vision = product_vision_path.relative_to(repo_root)
    rel_blueprint = solution_blueprint_path.relative_to(repo_root)

    brd_content = f"""# Business Requirements Document (BRD)
> **Generated:** {timestamp}
> **Status:** Compiled

---

## 1. Introduction
This document aggregates the approved product strategy, vision, and solution design into a single source of truth.

---

## 2. Market Strategy (Source: {rel_market})
{strategy_content}

---

## 3. Product Vision (Source: {rel_vision})
{vision_content}

---

## 4. Solution Blueprint (Source: {rel_blueprint})
{blueprint_content}

---

## 5. Appendices
- [Original Strategy]({rel_market})
- [Original Vision]({rel_vision})
- [Original Blueprint]({rel_blueprint})
"""

    output_path.write_text(brd_content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile product artifacts into a single BRD markdown file.",
    )
    parser.add_argument(
        "--market-file",
        required=True,
        help="Path to MARKET_STRATEGY.md (must be inside repository).",
    )
    parser.add_argument(
        "--vision-file",
        required=True,
        help="Path to PRODUCT_VISION.md (must be inside repository).",
    )
    parser.add_argument(
        "--blueprint-file",
        required=True,
        help="Path to SOLUTION_BLUEPRINT.md (must be inside repository).",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path to output BRD markdown file (must be inside repository).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = get_repo_root()

    try:
        market_path = resolve_markdown_read_path(args.market_file, repo_root)
        vision_path = resolve_markdown_read_path(args.vision_file, repo_root)
        blueprint_path = resolve_markdown_read_path(args.blueprint_file, repo_root)
        output_path = resolve_markdown_write_path(args.output_file, repo_root)

        compile_brd(market_path, vision_path, blueprint_path, output_path, repo_root)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"SUCCESS: BRD compiled at {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
