"""Validation script for the Claude for Financial Services Agent Company package."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent


class ValidationError(Exception):
    pass


REQUIRED_FIELDS: dict[str, set[str]] = {
    "company": {"schema", "kind", "slug", "name", "description", "version", "license", "authors"},
    "team": {"kind", "slug", "name", "description", "includes"},
    "agent": {"kind", "slug", "name", "title", "reportsTo", "skills"},
    "skill": {"kind", "slug", "name", "description"},
}


def validate_frontmatter(kind: str, fm: dict[str, Any]) -> None:
    required = REQUIRED_FIELDS.get(kind)
    if required is None:
        raise ValidationError(f"unknown kind: {kind}")
    missing = required - set(fm)
    if missing:
        raise ValidationError(f"{kind} missing required fields: {sorted(missing)}")
    if fm.get("kind") != kind:
        raise ValidationError(f"frontmatter kind={fm.get('kind')!r} does not match expected {kind!r}")


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        raise ValidationError("file does not start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValidationError("frontmatter is unterminated")
    return yaml.safe_load(text[4:end])


def check_cross_references(package_root: Path) -> None:
    skills_dir = package_root / "skills"
    available = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.exists() else set()

    agents_dir = package_root / "agents"
    if not agents_dir.exists():
        return
    for agent_md in agents_dir.glob("*/AGENTS.md"):
        fm = parse_frontmatter(agent_md.read_text())
        for skill in fm.get("skills", []):
            if skill not in available:
                raise ValidationError(
                    f"{agent_md.relative_to(package_root)}: references missing skill {skill!r}"
                )
