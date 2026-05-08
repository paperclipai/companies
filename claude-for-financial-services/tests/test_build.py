from pathlib import Path
from scripts.build import load_manifest


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
