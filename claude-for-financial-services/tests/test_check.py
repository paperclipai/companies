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
