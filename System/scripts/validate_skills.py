#!/usr/bin/env python3
"""Run skill validation across all local skills."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def discover_skill_dirs(skills_root: Path) -> list[Path]:
    if not skills_root.is_dir():
        return []

    return sorted(
        child for child in skills_root.iterdir() if child.is_dir() and (child / "SKILL.md").is_file()
    )


def validate_skills(repo_root: Path, validator: Path, skills_root: Path, quiet: bool) -> int:
    skill_dirs = discover_skill_dirs(skills_root)
    if not skill_dirs:
        print(f"No skills found under {skills_root}", file=sys.stderr)
        return 2

    failures = 0

    for skill_dir in skill_dirs:
        rel_skill = skill_dir.relative_to(repo_root).as_posix()
        cmd = [sys.executable, str(validator), str(skill_dir)]

        if quiet:
            result = subprocess.run(cmd, cwd=repo_root, check=False, capture_output=True, text=True)
            if result.returncode != 0:
                failures += 1
                print(f"FAIL: {rel_skill}")
                if result.stdout:
                    print(result.stdout.strip())
                if result.stderr:
                    print(result.stderr.strip(), file=sys.stderr)
            else:
                print(f"OK: {rel_skill}")
        else:
            print(f"Validating: {rel_skill}")
            result = subprocess.run(cmd, cwd=repo_root, check=False)
            if result.returncode != 0:
                failures += 1

    total = len(skill_dirs)
    passed = total - failures
    print(f"Skill validation summary: {passed}/{total} passed")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all skills in .agent/skills")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--skills-dir", default=".agent/skills", help="Skills directory relative to root")
    parser.add_argument(
        "--validator",
        default=".agent/skills/skill-creator/scripts/validate_skill.py",
        help="Path to validate_skill.py relative to root",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Capture per-skill output unless validation fails",
    )
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    skills_root = (repo_root / args.skills_dir).resolve()
    validator = (repo_root / args.validator).resolve()

    if not validator.is_file():
        print(f"Validator not found: {validator}", file=sys.stderr)
        return 2

    return validate_skills(repo_root, validator, skills_root, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
