from pathlib import Path

import pytest
import yaml

from scripts.check import validate_frontmatter, ValidationError


def test_validate_frontmatter_rejects_missing_required_field():
    bad = {"kind": "agent", "slug": "x"}  # missing name, description
    with pytest.raises(ValidationError, match="name"):
        validate_frontmatter("agent", bad)


def test_validate_frontmatter_accepts_complete_agent():
    good = {
        "kind": "agent", "slug": "x", "name": "X", "title": "X-er",
        "reportsTo": "../../teams/t/TEAM.md", "skills": ["s"],
    }
    validate_frontmatter("agent", good)  # no exception


from scripts.check import check_cross_references


def test_check_cross_references_rejects_missing_skill(tmp_path):
    # Build a tiny package where AGENTS.md references a missing skill
    (tmp_path / "agents" / "alpha").mkdir(parents=True)
    (tmp_path / "agents" / "alpha" / "AGENTS.md").write_text(
        "---\nkind: agent\nslug: alpha\nname: Alpha\ntitle: A\n"
        "reportsTo: ../../teams/t/TEAM.md\nskills: [does-not-exist]\n---\n"
    )
    (tmp_path / "skills").mkdir()  # empty
    with pytest.raises(ValidationError, match="does-not-exist"):
        check_cross_references(tmp_path)


def test_check_cross_references_passes_when_all_resolve(tmp_path):
    (tmp_path / "agents" / "alpha").mkdir(parents=True)
    (tmp_path / "agents" / "alpha" / "AGENTS.md").write_text(
        "---\nkind: agent\nslug: alpha\nname: Alpha\ntitle: A\n"
        "reportsTo: ../../teams/t/TEAM.md\nskills: [present]\n---\n"
    )
    (tmp_path / "skills" / "present").mkdir(parents=True)
    (tmp_path / "skills" / "present" / "SKILL.md").write_text(
        "---\nkind: skill\nslug: present\nname: P\ndescription: x\n---\n"
    )
    check_cross_references(tmp_path)  # no exception
