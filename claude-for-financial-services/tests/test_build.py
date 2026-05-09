import yaml
from pathlib import Path
from scripts.build import load_manifest, resolve_canonical_paths


def test_load_manifest_returns_structured_object(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    assert m.slug == "test-co"
    assert m.upstream.commit == "deadbeef"
    assert "alpha" in m.agents
    assert m.agents["alpha"].team == "team-a"
    assert m.agents["alpha"].skills == ["skill-1"]
    assert "skill-1" in m.skills
    assert "team-a" in m.teams


def test_resolve_canonical_paths_picks_alphabetical_when_dates_equal():
    # Mock upstream owners and per-file commit dates
    skill_owners = {
        "xlsx-author": ["zebra", "earnings-reviewer", "alpha"],
        "dcf-model": ["model-builder", "pitch-agent"],
        "kyc-rules": ["kyc-screener"],
    }
    # All same date — tiebreak by alphabetical agent name
    file_dates = {
        ("zebra", "xlsx-author"): "2026-05-07T00:00:00Z",
        ("earnings-reviewer", "xlsx-author"): "2026-05-07T00:00:00Z",
        ("alpha", "xlsx-author"): "2026-05-07T00:00:00Z",
        ("model-builder", "dcf-model"): "2026-05-06T00:00:00Z",
        ("pitch-agent", "dcf-model"): "2026-05-07T00:00:00Z",
        ("kyc-screener", "kyc-rules"): "2026-05-01T00:00:00Z",
    }
    result = resolve_canonical_paths(skill_owners, file_dates)
    assert result["xlsx-author"] == "alpha"
    assert result["dcf-model"] == "pitch-agent"  # most-recent wins
    assert result["kyc-rules"] == "kyc-screener"  # only owner


from scripts.build import compute_content_hash


def test_compute_content_hash_is_sha256_hex():
    content = b"hello world"
    h = compute_content_hash(content)
    # `sha256("hello world")` = b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
    assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


import yaml
from scripts.build import emit_company, load_manifest


def test_emit_company_produces_valid_yaml_frontmatter(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    out_path = tmp_path / "COMPANY.md"
    emit_company(m, out_path)

    text = out_path.read_text()
    assert text.startswith("---\n")
    fm_end = text.find("\n---\n", 4)
    assert fm_end > 0
    fm = yaml.safe_load(text[4:fm_end])

    assert fm["schema"] == "agentcompanies/v1"
    assert "kind" not in fm
    assert fm["slug"] == "test-co"
    assert fm["license"] == "Apache-2.0"
    assert fm["metadata"]["upstream"]["commit"] == "deadbeef"
    body = text[fm_end + len("\n---\n"):]
    assert "Test Co" in body


from scripts.build import emit_teams


def test_emit_teams_creates_one_file_per_team(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    emit_teams(m, tmp_path)

    team_path = tmp_path / "team-a" / "TEAM.md"
    assert team_path.exists()
    text = team_path.read_text()
    fm_end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:fm_end])
    assert "kind" not in fm
    assert fm["slug"] == "team-a"
    assert fm["includes"] == ["../../agents/alpha/AGENTS.md"]


from scripts.build import emit_agents


def test_emit_agents_creates_one_file_per_agent_with_skill_list(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    emit_agents(m, tmp_path)

    agent_path = tmp_path / "alpha" / "AGENTS.md"
    assert agent_path.exists()
    text = agent_path.read_text()
    fm_end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:fm_end])
    assert "kind" not in fm
    assert fm["slug"] == "alpha"
    assert fm["title"] == "Alpha Agent"
    assert fm["reportsTo"] == "../../teams/team-a/TEAM.md"
    assert fm["skills"] == ["skill-1"]
    assert fm["metadata"]["sources"][0]["url"] == \
        "https://github.com/example/upstream/tree/deadbeef/plugins/agent-plugins/alpha"

    body = text[fm_end + len("\n---\n"):]
    assert "Test agent" in body


from scripts.build import emit_skills, emit_org_chart_dot


def test_emit_org_chart_dot_contains_all_agents_and_teams():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    dot = emit_org_chart_dot(m)
    assert "digraph" in dot
    assert '"team-a"' in dot
    assert '"alpha"' in dot
    assert '"team-a" -> "alpha"' in dot


def test_emit_skills_creates_one_file_per_skill_with_canonical_path(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)

    canonical = {"skill-1": "alpha"}  # canonical owner per skill
    hashes = {"skill-1": "abc123"}    # content hash per skill

    emit_skills(m, canonical, hashes, tmp_path)

    skill_path = tmp_path / "skill-1" / "SKILL.md"
    assert skill_path.exists()
    text = skill_path.read_text()
    fm_end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:fm_end])
    assert "kind" not in fm
    assert fm["slug"] == "skill-1"
    src = fm["metadata"]["sources"][0]
    assert src["repo"] == "example/upstream"
    assert src["commit"] == "deadbeef"
    assert src["path"] == "plugins/agent-plugins/alpha/skills/skill-1/SKILL.md"
    assert src["mode"] == "referenced"
    assert src["contentHash"] == "abc123"
