from pathlib import Path

import pytest
import yaml

from scripts.check import validate_frontmatter, ValidationError, check_content_hashes


def test_validate_frontmatter_rejects_missing_required_field():
    bad = {"slug": "x", "title": "X-er", "reportsTo": "../../teams/t/TEAM.md", "skills": ["s"]}  # missing name
    with pytest.raises(ValidationError, match="name"):
        validate_frontmatter("agent", bad)


def test_validate_frontmatter_accepts_complete_agent():
    good = {
        "slug": "x", "name": "X", "title": "X-er",
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


def test_check_content_hashes_passes_when_hash_matches(tmp_path, monkeypatch):
    (tmp_path / "skills" / "s1").mkdir(parents=True)
    (tmp_path / "skills" / "s1" / "SKILL.md").write_text(
        "---\nkind: skill\nslug: s1\nname: S\ndescription: x\n"
        "metadata:\n  sources:\n    - repo: example/u\n      commit: deadbeef\n"
        "      path: plugins/agent-plugins/a/skills/s1/SKILL.md\n      mode: referenced\n"
        "      contentHash: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9\n---\n"
    )

    def fake_fetch(repo, commit, path):
        return b"hello world"

    monkeypatch.setattr("scripts.check.fetch_upstream_file", fake_fetch)
    check_content_hashes(tmp_path)  # no exception


def test_check_content_hashes_rejects_stale_hash(tmp_path, monkeypatch):
    (tmp_path / "skills" / "s1").mkdir(parents=True)
    (tmp_path / "skills" / "s1" / "SKILL.md").write_text(
        "---\nkind: skill\nslug: s1\nname: S\ndescription: x\n"
        "metadata:\n  sources:\n    - repo: example/u\n      commit: deadbeef\n"
        "      path: plugins/agent-plugins/a/skills/s1/SKILL.md\n      mode: referenced\n"
        "      contentHash: 0000000000000000000000000000000000000000000000000000000000000000\n---\n"
    )
    monkeypatch.setattr("scripts.check.fetch_upstream_file", lambda r, c, p: b"hello world")
    with pytest.raises(ValidationError, match="contentHash"):
        check_content_hashes(tmp_path)
