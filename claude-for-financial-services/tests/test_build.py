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
