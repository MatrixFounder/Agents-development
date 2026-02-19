#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

IGNORE_PATH_PARTS = {
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".git",
}
IGNORE_FILENAMES = {
    ".DS_Store",
    "package-lock.json",
    "yarn.lock",
}
IGNORE_SUFFIXES = (
    ".min.js",
    ".min.css",
    ".map",
    ".lock",
    ".pyc",
)
SOURCE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".swift",
    ".ts",
    ".tsx",
}
SOURCE_FILENAMES = {
    "Dockerfile",
}
SOURCE_DIR_HINTS = {
    "api",
    "app",
    "backend",
    "client",
    "frontend",
    "lib",
    "pkg",
    "server",
    "services",
    "src",
}
DEFAULT_DEVELOPMENT_ROOTS = ("src",)
BLOCKED_MEMORY_PREFIXES = (
    ".agent/skills",
    ".cursor/skills",
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


def _run_git_lines(repo_root: Path, args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _collect_unique(repo_root: Path, commands: list[list[str]]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    for args in commands:
        for rel_path in _run_git_lines(repo_root, args):
            if rel_path in seen:
                continue
            seen.add(rel_path)
            ordered.append(rel_path)

    return ordered


def get_changed_files(repo_root: Path) -> list[str]:
    commands = [
        ["diff", "--name-only", "--staged"],
        ["diff", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ]
    return _collect_unique(repo_root, commands)


def get_all_files(repo_root: Path) -> list[str]:
    commands = [
        ["ls-files"],
        ["ls-files", "--others", "--exclude-standard"],
    ]
    files = _collect_unique(repo_root, commands)
    if files:
        return files

    # Fallback when repository metadata is unavailable.
    collected: list[str] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        collected.append(path.relative_to(repo_root).as_posix())
    return collected


def _is_ignored(rel_path: str) -> bool:
    path = Path(rel_path)

    if any(part in IGNORE_PATH_PARTS for part in path.parts):
        return True

    if path.name in IGNORE_FILENAMES:
        return True

    normalized = rel_path.replace("\\", "/")
    if any(normalized.endswith(suffix) for suffix in IGNORE_SUFFIXES):
        return True

    return False


def _is_source_candidate(rel_path: str) -> bool:
    path = Path(rel_path)
    suffix = path.suffix.lower()
    if suffix in SOURCE_SUFFIXES:
        return True
    if path.name in SOURCE_FILENAMES:
        return True
    return any(part in SOURCE_DIR_HINTS for part in path.parts)


def _normalize_rel_prefix(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    normalized = normalized.strip("/")
    return normalized or "."


def _normalize_development_roots(values: list[str] | None) -> list[str]:
    roots = values if values else list(DEFAULT_DEVELOPMENT_ROOTS)
    normalized: list[str] = []
    seen: set[str] = set()
    for value in roots:
        root = _normalize_rel_prefix(value)
        if root in seen:
            continue
        seen.add(root)
        normalized.append(root)
    return normalized


def _in_development_scope(rel_path: str, development_roots: list[str]) -> bool:
    normalized = _normalize_rel_prefix(rel_path)
    for blocked in BLOCKED_MEMORY_PREFIXES:
        if normalized == blocked or normalized.startswith(f"{blocked}/"):
            return False
    for root in development_roots:
        if root == ".":
            return True
        if normalized == root or normalized.startswith(f"{root}/"):
            return True
    return False


def find_existing_agents_file(file_path: str, repo_root: Path) -> Path | None:
    candidate_path = (repo_root / file_path).resolve(strict=False).parent

    while True:
        candidate = candidate_path / ".AGENTS.md"
        if candidate.exists():
            return candidate

        if candidate_path == repo_root:
            break

        try:
            candidate_path.relative_to(repo_root)
        except ValueError:
            break

        candidate_path = candidate_path.parent

    return None


def resolve_target_agents_file(
    file_path: str,
    repo_root: Path,
    include_non_source: bool,
    development_roots: list[str],
) -> Path | None:
    if not _in_development_scope(file_path, development_roots):
        return None

    existing = find_existing_agents_file(file_path, repo_root)
    if existing is not None:
        return existing

    if not include_non_source and not _is_source_candidate(file_path):
        return None

    return (repo_root / file_path).resolve(strict=False).parent / ".AGENTS.md"


def group_by_target(
    files: list[str],
    repo_root: Path,
    include_non_source: bool,
    development_roots: list[str],
) -> dict[Path, list[str]]:
    grouped: dict[Path, list[str]] = defaultdict(list)

    for rel_path in files:
        if _is_ignored(rel_path):
            continue

        target = resolve_target_agents_file(
            rel_path,
            repo_root,
            include_non_source,
            development_roots,
        )
        if target is None:
            continue

        grouped[target].append(rel_path)

    return grouped


def _render_agents_skeleton() -> str:
    return (
        "# Local Agent Memory\n\n"
        "This file stores context for this source-code directory.\n\n"
        "## Components\n\n"
        "<!-- Add purpose, key classes/functions, and constraints. -->\n"
    )


def create_missing_agents_files(targets: list[Path]) -> list[Path]:
    created: list[Path] = []
    for target in targets:
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_agents_skeleton(), encoding="utf-8")
        created.append(target)
    return created


def print_suggestions(grouped: dict[Path, list[str]], repo_root: Path) -> None:
    for target in sorted(grouped.keys(), key=lambda path: str(path)):
        try:
            target_label = target.relative_to(repo_root)
        except ValueError:
            target_label = target

        print(f"\n### Target: {target_label}")
        print("Suggested Updates:\n")

        for rel_path in grouped[target]:
            fname = Path(rel_path).name
            print(f"#### [{fname}]")
            print(f"**Purpose:** [Update purpose for {fname}]")
            print("**Classes/Functions:**")
            print("- `ClassName` - [Description]")
            print()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Suggest .AGENTS.md updates from repository files.",
    )
    parser.add_argument(
        "--mode",
        choices=("changes", "bootstrap"),
        default="changes",
        help=(
            "changes: inspect staged/unstaged/untracked files; "
            "bootstrap: inspect all repository files."
        ),
    )
    parser.add_argument(
        "--create-missing",
        action="store_true",
        help="Create missing .AGENTS.md target files (existing files are preserved).",
    )
    parser.add_argument(
        "--include-non-source",
        action="store_true",
        help="When no target exists, include non-source files as target candidates.",
    )
    parser.add_argument(
        "--development-root",
        action="append",
        dest="development_roots",
        default=None,
        help=(
            "Relative path prefix for intentional project development scope. "
            "Repeat flag for multiple roots. Default: src"
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv or sys.argv[1:])
        repo_root = get_repo_root()
        development_roots = _normalize_development_roots(args.development_roots)
        files = (
            get_changed_files(repo_root)
            if args.mode == "changes"
            else get_all_files(repo_root)
        )
        if not files:
            print(f"No files found for mode={args.mode}.")
            return 0

        grouped = group_by_target(
            files,
            repo_root,
            args.include_non_source,
            development_roots,
        )
        if not grouped:
            roots_label = ", ".join(development_roots)
            print(
                "No candidate .AGENTS.md targets found "
                f"inside development root(s): {roots_label}"
            )
            return 0

        if args.create_missing:
            created = create_missing_agents_files(list(grouped.keys()))
            if created:
                print(f"Created {len(created)} missing .AGENTS.md file(s).")
            else:
                print("No missing .AGENTS.md files to create.")

        total_files = sum(len(file_list) for file_list in grouped.values())
        print(
            f"Found {total_files} candidate files across {len(grouped)} target(s) "
            f"(mode={args.mode}, roots={','.join(development_roots)})."
        )
        print_suggestions(grouped, repo_root)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
