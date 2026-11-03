#!/usr/bin/env python3
"""Validate every skill in skills/ against the Agent Skills specification.

Usage:
    pip install skills-ref
    python scripts/validate.py

Exits non-zero when any skill fails validation.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

MAX_SKILL_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 512 * 1024
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def size_problems(skill_dir: Path) -> list[str]:
    """Flag oversized files and skills."""
    problems: list[str] = []
    total = 0
    for path in skill_dir.rglob("*"):
        if not path.is_file() or SKIP_DIRS & set(path.parts):
            continue
        size = path.stat().st_size
        total += size
        if size > MAX_FILE_BYTES:
            problems.append(
                f"{path.relative_to(ROOT).as_posix()} is {size / 1024:.0f} KB, max is 512 KB"
            )
    if total > MAX_SKILL_BYTES:
        problems.append(
            f"{skill_dir.relative_to(ROOT).as_posix()} is {total / 1024 / 1024:.1f} MB, max is 2 MB"
        )
    return problems


def main() -> int:
    try:
        from skills_ref import validate
    except ImportError:
        print("skills-ref is not installed. Run: pip install skills-ref", file=sys.stderr)
        return 2

    if not SKILLS_DIR.is_dir():
        print(f"No skills directory at {SKILLS_DIR}", file=sys.stderr)
        return 2

    skill_dirs = sorted(
        path
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    if not skill_dirs:
        print("skills/ is empty — nothing to validate.")
        return 0

    failures = 0
    for skill_dir in skill_dirs:
        problems = list(validate(skill_dir)) + size_problems(skill_dir)
        if problems:
            failures += 1
            print(f"FAIL {skill_dir.name}")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"ok   {skill_dir.name}")

    print()
    if failures:
        print(f"{failures} of {len(skill_dirs)} skill(s) failed validation")
        return 1
    print(f"All {len(skill_dirs)} skill(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
