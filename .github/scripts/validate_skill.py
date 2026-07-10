#!/usr/bin/env python3
"""Validate ODIA Cortex Skill folders.

The validator intentionally avoids external dependencies so it can run locally
and in GitHub Actions without package installation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "id",
    "name",
    "title",
    "summary",
    "description",
    "authors",
    "owner_agency",
    "status",
    "categories",
    "data_classification",
    "tools",
    "prompt",
    "language",
]

VALID_STATUSES = {"draft", "beta", "stable", "archived"}
VALID_DATA_CLASSIFICATIONS = {"public", "internal", "restricted", "confidential"}
LICENSE_MARKERS = ("apache license", "commonwealth", "odia", "mit license")
SECRET_PATTERNS = [
    re.compile(r"password\s*[:=]", re.IGNORECASE),
    re.compile(r"secret\s*[:=]", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]", re.IGNORECASE),
    re.compile(r"token\s*[:=]", re.IGNORECASE),
    re.compile(r"-----BEGIN (RSA |OPENSSH |)PRIVATE KEY-----"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Cortex Skill folders.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate every real skill directory under skills/.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional skill directories to validate.",
    )
    return parser.parse_args()


def find_skill_dirs(root: Path, args: argparse.Namespace) -> list[Path]:
    if args.paths:
        return [Path(path) for path in args.paths]

    skills_root = root / "skills"
    if not skills_root.exists():
        return []

    skill_dirs = []
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("_"):
            continue
        skill_dirs.append(child)
    return skill_dirs


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, str], str | None]:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, "SKILL.md must start with YAML frontmatter delimited by ---"

    end = content.find("\n---", 3)
    if end == -1:
        return {}, "SKILL.md frontmatter must close with ---"

    raw = content[3:end].strip("\n")
    values: dict[str, str] = {}
    current_key: str | None = None

    for raw_line in raw.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        is_continuation = raw_line.startswith((" ", "\t", "-"))
        if is_continuation and current_key:
            values[current_key] = (values.get(current_key, "") + "\n" + raw_line.strip()).strip()
            continue

        if ":" not in raw_line:
            if current_key:
                values[current_key] = (values.get(current_key, "") + "\n" + raw_line.strip()).strip()
                continue
            return values, f"Could not parse frontmatter line: {raw_line}"

        key, value = raw_line.split(":", 1)
        current_key = key.strip()
        values[current_key] = value.strip().strip('"').strip("'")

    return values, None


def check_for_secret_patterns(skill_dir: Path) -> list[str]:
    warnings = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                warnings.append(f"{path}: possible secret-like text matched {pattern.pattern!r}")
    return warnings


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.exists() or not skill_dir.is_dir():
        return [f"{skill_dir} is not a directory"], warnings

    skill_md = skill_dir / "SKILL.md"
    license_file = skill_dir / "LICENSE"

    if not skill_md.exists():
        errors.append("Missing SKILL.md")
        frontmatter = {}
    else:
        frontmatter, parse_error = parse_frontmatter(skill_md)
        if parse_error:
            errors.append(parse_error)

        for field in REQUIRED_FIELDS:
            if not frontmatter.get(field):
                errors.append(f"Missing required frontmatter field: {field}")

        skill_id = frontmatter.get("id")
        if skill_id and skill_id != skill_dir.name:
            errors.append(f"Frontmatter id {skill_id!r} must match folder name {skill_dir.name!r}")
        if skill_id and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
            errors.append("Frontmatter id must use lowercase letters, numbers, and hyphens")

        skill_name = frontmatter.get("name")
        if skill_name and skill_id and skill_name != skill_id:
            warnings.append("Frontmatter name should match id unless there is a clear reason")

        status = frontmatter.get("status")
        if status and status not in VALID_STATUSES:
            errors.append(f"Status {status!r} must be one of {sorted(VALID_STATUSES)}")

        data_classification = frontmatter.get("data_classification")
        if data_classification and data_classification not in VALID_DATA_CLASSIFICATIONS:
            warnings.append(
                f"data_classification {data_classification!r} is not one of "
                f"{sorted(VALID_DATA_CLASSIFICATIONS)}"
            )

    if not license_file.exists():
        errors.append("Missing LICENSE")
    else:
        license_text = license_file.read_text(encoding="utf-8").lower()
        if not any(marker in license_text for marker in LICENSE_MARKERS):
            errors.append("LICENSE should include an approved license marker")

    warnings.extend(check_for_secret_patterns(skill_dir))
    return errors, warnings


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    skill_dirs = find_skill_dirs(root, args)

    if not skill_dirs:
        print("No skill directories found.")
        return 0

    failed = False
    for skill_dir in skill_dirs:
        print(f"\n--- Validating {skill_dir} ---")
        errors, warnings = validate_skill(skill_dir)

        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")

        if errors:
            failed = True
            print("FAILED")
        else:
            print("PASSED")

    if failed:
        print("\nSkill validation failed.")
        return 1

    print("\nSkill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

