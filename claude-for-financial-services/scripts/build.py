"""Build script for the Claude for Financial Services Agent Company package.

Generates COMPANY.md, TEAM.md, AGENTS.md, SKILL.md files plus the org-chart
image from the canonical manifest.yaml.
"""
from __future__ import annotations

import base64
import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Author:
    name: str
    email: str


@dataclass
class Upstream:
    repo: str
    commit: str
    license: str


@dataclass
class Team:
    name: str
    description: str


@dataclass
class Agent:
    name: str
    title: str
    team: str
    description: str
    skills: list[str]


@dataclass
class Skill:
    name: str
    description: str


@dataclass
class Manifest:
    schema: str
    slug: str
    name: str
    description: str
    version: str
    license: str
    authors: list[Author]
    goals: list[str]
    tags: list[str]
    upstream: Upstream
    affiliation: str
    teams: dict[str, Team]
    agents: dict[str, Agent]
    skills: dict[str, Skill]


def load_manifest(path: Path) -> Manifest:
    raw: dict[str, Any] = yaml.safe_load(path.read_text())
    return Manifest(
        schema=raw["schema"],
        slug=raw["slug"],
        name=raw["name"],
        description=raw["description"],
        version=raw["version"],
        license=raw["license"],
        authors=[Author(**a) for a in raw["authors"]],
        goals=list(raw["goals"]),
        tags=list(raw["tags"]),
        upstream=Upstream(**raw["upstream"]),
        affiliation=raw["affiliation"],
        teams={k: Team(**v) for k, v in raw["teams"].items()},
        agents={k: Agent(**v) for k, v in raw["agents"].items()},
        skills={k: Skill(**v) for k, v in raw["skills"].items()},
    )


def resolve_canonical_paths(
    skill_owners: dict[str, list[str]],
    file_dates: dict[tuple[str, str], str],
) -> dict[str, str]:
    """For each skill, pick the canonical upstream agent owner.

    Rule: most-recent file commit date wins; alphabetical agent name on ties.
    """
    result: dict[str, str] = {}
    for skill, owners in skill_owners.items():
        most_recent_date = max(file_dates[(a, skill)] for a in owners)
        tied = [a for a in owners if file_dates[(a, skill)] == most_recent_date]
        result[skill] = sorted(tied)[0]
    return result


def fetch_upstream_skill_inventory(
    repo: str, commit: str
) -> tuple[dict[str, list[str]], dict[tuple[str, str], str]]:
    """Discover SKILL.md files under upstream agent-plugins at the pinned commit.

    Returns (skill_owners, file_dates) where:
      skill_owners[skill_slug] = [agent_slug, ...]
      file_dates[(agent_slug, skill_slug)] = ISO 8601 commit date for that file
    """
    # List all SKILL.md files at the pinned tree
    tree = subprocess.run(
        ["gh", "api", f"repos/{repo}/git/trees/{commit}?recursive=1", "--jq",
         '.tree[] | select(.path | test("plugins/agent-plugins/[^/]+/skills/[^/]+/SKILL\\\\.md$")) | .path'],
        check=True, capture_output=True, text=True,
    )
    skill_owners: dict[str, list[str]] = {}
    paths: list[tuple[str, str, str]] = []  # (agent, skill, full_path)
    for line in tree.stdout.splitlines():
        parts = line.split("/")
        # plugins/agent-plugins/<agent>/skills/<skill>/SKILL.md
        agent, skill = parts[2], parts[4]
        skill_owners.setdefault(skill, []).append(agent)
        paths.append((agent, skill, line))

    # Fetch the most-recent commit date touching each file
    file_dates: dict[tuple[str, str], str] = {}
    for agent, skill, path in paths:
        out = subprocess.run(
            ["gh", "api", f"repos/{repo}/commits?path={path}&sha={commit}&per_page=1",
             "--jq", ".[0].commit.committer.date"],
            check=True, capture_output=True, text=True,
        )
        file_dates[(agent, skill)] = out.stdout.strip()

    return skill_owners, file_dates


def compute_content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fetch_upstream_file(repo: str, commit: str, path: str) -> bytes:
    """Fetch raw bytes of a file from upstream at the pinned commit."""
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={commit}", "--jq", ".content"],
        check=True, capture_output=True, text=True,
    )
    return base64.b64decode(out.stdout.strip())


def _frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"


def emit_company(m: Manifest, out_path: Path) -> None:
    fm = {
        "schema": m.schema,
        "slug": m.slug,
        "name": m.name,
        "description": m.description,
        "version": m.version,
        "license": m.license,
        "authors": [{"name": a.name, "email": a.email} for a in m.authors],
        "goals": m.goals,
        "tags": m.tags,
        "metadata": {
            "upstream": {
                "repo": m.upstream.repo,
                "commit": m.upstream.commit,
                "license": m.upstream.license,
            },
            "affiliation": m.affiliation,
        },
    }
    body_lines = [
        f"# {m.name}",
        "",
        m.description,
        "",
        "## Boundaries",
        "",
        "Nothing in this package constitutes investment, legal, tax, or accounting advice.",
        "These agents draft analyst work product (models, memos, research notes,",
        "reconciliations) for review by a qualified professional. They do not make",
        "investment recommendations, execute transactions, bind risk, post to a ledger,",
        "or approve onboarding; every output is staged for human sign-off.",
        "",
        "## Teams",
        "",
    ]
    for slug, team in m.teams.items():
        body_lines.append(f"- **{team.name}** (`teams/{slug}/TEAM.md`) — {team.description}")
    body_lines.append("")
    out_path.write_text(_frontmatter(fm) + "\n".join(body_lines) + "\n")


def emit_teams(m: Manifest, teams_root: Path) -> None:
    # Build team -> [agent_slug] mapping from agents
    team_agents: dict[str, list[str]] = {t: [] for t in m.teams}
    for agent_slug, agent in m.agents.items():
        team_agents[agent.team].append(agent_slug)

    for slug, team in m.teams.items():
        out_dir = teams_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "slug": slug,
            "name": team.name,
            "description": team.description,
            "includes": [
                f"../../agents/{a}/AGENTS.md" for a in sorted(team_agents[slug])
            ],
        }
        body = f"\n# {team.name}\n\n{team.description}\n"
        (out_dir / "TEAM.md").write_text(_frontmatter(fm) + body)


def emit_agents(m: Manifest, agents_root: Path) -> None:
    for slug, agent in m.agents.items():
        out_dir = agents_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "slug": slug,
            "name": agent.name,
            "title": agent.title,
            "reportsTo": f"../../teams/{agent.team}/TEAM.md",
            "skills": list(agent.skills),
            "tags": ["finance", agent.team],
            "metadata": {
                "sources": [
                    {
                        "url": f"https://github.com/{m.upstream.repo}/tree/{m.upstream.commit}/plugins/agent-plugins/{slug}",
                        "mode": "referenced",
                    }
                ]
            },
        }
        body = f"\n# {agent.name}\n\n{agent.description.strip()}\n"
        (out_dir / "AGENTS.md").write_text(_frontmatter(fm) + body)


def emit_skills(
    m: Manifest,
    canonical_owner: dict[str, str],
    content_hashes: dict[str, str],
    skills_root: Path,
) -> None:
    for slug, skill in m.skills.items():
        owner = canonical_owner[slug]
        upstream_path = f"plugins/agent-plugins/{owner}/skills/{slug}/SKILL.md"
        out_dir = skills_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "slug": slug,
            "name": skill.name,
            "description": skill.description,
            "version": "0.1.0",
            "metadata": {
                "sources": [
                    {
                        "repo": m.upstream.repo,
                        "commit": m.upstream.commit,
                        "path": upstream_path,
                        "mode": "referenced",
                        "contentHash": content_hashes[slug],
                    }
                ]
            },
        }
        body = (
            f"\n# {skill.name}\n\n"
            f"> Skill content lives upstream at the path above (commit `{m.upstream.commit}`).\n"
            f"> Pull the upstream file before invocation; do not edit this manifest in place.\n"
        )
        (out_dir / "SKILL.md").write_text(_frontmatter(fm) + body)


def emit_org_chart_dot(m: Manifest) -> str:
    lines = [
        "digraph org {",
        "  rankdir=TB;",
        '  node [shape=box, style=rounded, fontname="Helvetica"];',
        f'  "{m.slug}" [label="{m.name}", style="rounded,filled", fillcolor="#e8f0fe"];',
    ]
    for team_slug, team in m.teams.items():
        lines.append(f'  "{team_slug}" [label="{team.name}", fillcolor="#fef3c7", style="rounded,filled"];')
        lines.append(f'  "{m.slug}" -> "{team_slug}";')
    for agent_slug, agent in m.agents.items():
        lines.append(f'  "{agent_slug}" [label="{agent.name}"];')
        lines.append(f'  "{agent.team}" -> "{agent_slug}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_org_chart(dot_text: str, out_png: Path) -> None:
    """Render `dot_text` to a PNG via the `dot` CLI."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["dot", "-Tpng", "-o", str(out_png)],
        input=dot_text, text=True, check=True,
    )


def main() -> None:
    m = load_manifest(ROOT / "manifest.yaml")
    print(f"Building {m.slug} v{m.version} from manifest…")

    skill_owners, file_dates = fetch_upstream_skill_inventory(m.upstream.repo, m.upstream.commit)
    canonical = resolve_canonical_paths(skill_owners, file_dates)

    # Filter canonical to only skills declared in our manifest
    canonical = {k: v for k, v in canonical.items() if k in m.skills}

    # Compute content hashes for each declared skill at the canonical path
    hashes: dict[str, str] = {}
    for slug, owner in canonical.items():
        path = f"plugins/agent-plugins/{owner}/skills/{slug}/SKILL.md"
        content = fetch_upstream_file(m.upstream.repo, m.upstream.commit, path)
        hashes[slug] = compute_content_hash(content)
        print(f"  hashed {slug} ← {path}")

    # Verify every declared skill has a canonical owner
    missing = set(m.skills) - set(canonical)
    if missing:
        raise SystemExit(f"Skills declared in manifest but missing upstream: {sorted(missing)}")

    emit_company(m, ROOT / "COMPANY.md")
    emit_teams(m, ROOT / "teams")
    emit_agents(m, ROOT / "agents")
    emit_skills(m, canonical, hashes, ROOT / "skills")

    dot = emit_org_chart_dot(m)
    (ROOT / "images").mkdir(exist_ok=True)
    (ROOT / "images" / "org-chart.dot").write_text(dot)
    render_org_chart(dot, ROOT / "images" / "org-chart.png")

    print("Build complete.")


if __name__ == "__main__":
    main()
