# Claude for Financial Services Agent Companies Port — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port `anthropics/financial-services@57772c3f` into the Agent Companies format and submit one PR adding `claude-for-financial-services/` to the `paperclipai/companies` catalog.

**Architecture:** A single canonical `manifest.yaml` lists agents, teams, skills, and the pinned upstream SHA. Two Python scripts (`scripts/build.py`, `scripts/check.py`) generate and validate the 46 manifest files (1 COMPANY + 4 TEAM + 10 AGENTS + 31 SKILL) plus the org-chart image. All upstream skill content is referenced by SHA, never vendored. The package gets built directly inside a fork of the catalog so the new-company addition and the catalog-root README edit ship in the same PR.

**Tech Stack:** Python 3.11+, PyYAML, pytest, graphviz CLI, `gh` CLI for upstream fetches, Make.

**Spec:** [`docs/superpowers/specs/2026-05-09-agent-company-port-design.md`](../specs/2026-05-09-agent-company-port-design.md)

---

## Task 0: Set up the working directory

**Files:**
- Create: `~/code/paperclipai-companies/` (clone of fork)
- Create: `~/code/paperclipai-companies/claude-for-financial-services/` (the new company dir)
- Move: `~/code/claude-fsi-agent-company/docs/superpowers/specs/2026-05-09-agent-company-port-design.md` → into the new company dir
- Move: this plan file → into the new company dir

- [ ] **Step 1: Fork the catalog repo on GitHub**

```bash
gh repo fork paperclipai/companies --clone=false
```

Expected: `✓ Created fork <your-username>/companies`

- [ ] **Step 2: Clone the fork locally**

```bash
mkdir -p ~/code && cd ~/code
gh repo clone <your-username>/companies paperclipai-companies
cd paperclipai-companies
git remote add upstream https://github.com/paperclipai/companies.git
git fetch upstream
git checkout -b add-claude-for-financial-services upstream/master
```

Expected: branch `add-claude-for-financial-services` checked out, tracking nothing.

- [ ] **Step 3: Create the company directory and move the spec/plan in**

```bash
mkdir -p claude-for-financial-services/docs/superpowers/{specs,plans}
mkdir -p claude-for-financial-services/{scripts,tests/fixtures,teams,agents,skills,images}
mv ~/code/claude-fsi-agent-company/docs/superpowers/specs/2026-05-09-agent-company-port-design.md \
   claude-for-financial-services/docs/superpowers/specs/
mv ~/code/claude-fsi-agent-company/docs/superpowers/plans/2026-05-09-agent-company-port-implementation.md \
   claude-for-financial-services/docs/superpowers/plans/
```

Expected: `ls claude-for-financial-services/docs/superpowers/specs/` shows the spec file.

- [ ] **Step 4: Commit the initial scaffolding**

```bash
cd ~/code/paperclipai-companies
git add claude-for-financial-services/
git commit -m "scaffold: claude-for-financial-services directory and design docs"
```

Expected: one commit on branch `add-claude-for-financial-services`.

---

## Task 1: Author `manifest.yaml`, `LICENSE`, `NOTICE`

**Files:**
- Create: `claude-for-financial-services/manifest.yaml`
- Create: `claude-for-financial-services/LICENSE`
- Create: `claude-for-financial-services/NOTICE`

- [ ] **Step 1: Write `manifest.yaml`**

Path: `claude-for-financial-services/manifest.yaml`

```yaml
schema: agentcompanies/v1
slug: claude-for-financial-services
name: Claude for Financial Services
description: 10-agent finance company — coverage, research, fund admin, and onboarding — ported from anthropics/financial-services into the Agent Companies format.
version: 0.1.0
license: Apache-2.0
authors:
  - name: Jannes Stubbemann
    email: jannes@aqora.io
goals:
  - Draft analyst work product (models, memos, reconciliations) for human review.
  - Cover the four FSI workflow areas Anthropic shipped — coverage & advisory, research & modeling, fund admin & finance ops, operations & onboarding.
  - Stage every output for human sign-off — no agent here executes trades, posts to a ledger, or approves onboarding.
tags: [finance, fsi, investment-banking, equity-research, private-equity, fund-admin, kyc]

upstream:
  repo: anthropics/financial-services
  commit: 57772c3f1607229fba0270f94abf3c976bbd852f
  license: Apache-2.0

affiliation: "Community port. Not affiliated with or endorsed by Anthropic."

teams:
  coverage-advisory:
    name: Coverage & Advisory
    description: Client-facing pitch and meeting workflows.
  research-modeling:
    name: Research & Modeling
    description: Sector research, earnings, and live financial modeling in Excel.
  fund-admin-finance-ops:
    name: Fund Admin & Finance Ops
    description: Valuation, close, and statement workflows for fund administrators.
  operations-onboarding:
    name: Operations & Onboarding
    description: KYC and client onboarding workflows.

agents:
  pitch-agent:
    name: Pitch Agent
    title: Coverage Pitch Builder
    team: coverage-advisory
    description: |
      Builds target lists, runs comps and precedents, drafts an LBO, and assembles
      a branded pitchbook end to end. Output is a deck plus underlying models,
      staged for banker review before it goes to a client.
    skills: [3-statement-model, audit-xls, comps-analysis, dcf-model, deck-refresh, ib-check-deck, lbo-model, pitch-deck, pptx-author, sector-overview, xlsx-author]
  meeting-prep-agent:
    name: Meeting Prep Agent
    title: Client Meeting Briefing Builder
    team: coverage-advisory
    description: |
      Assembles a briefing pack before every client meeting — counterparty profile,
      recent activity, talking points, and proposal options. Staged for banker
      review.
    skills: [client-report, client-review, investment-proposal, pptx-author]
  market-researcher:
    name: Market Researcher
    title: Sector & Theme Research Analyst
    team: research-modeling
    description: |
      Turns a sector or theme into an industry overview, competitive landscape,
      peer comps, and an ideas shortlist. Drafts research; staged for analyst
      sign-off.
    skills: [competitive-analysis, comps-analysis, idea-generation, pptx-author, sector-overview]
  earnings-reviewer:
    name: Earnings Reviewer
    title: Earnings Call & Filings Reviewer
    team: research-modeling
    description: |
      Reads earnings call transcripts and filings, updates the model, drafts a
      morning note, and flags thesis changes. Staged for analyst sign-off.
    skills: [audit-xls, earnings-analysis, earnings-preview, model-update, morning-note, xlsx-author]
  model-builder:
    name: Model Builder
    title: Financial Model Builder
    team: research-modeling
    description: |
      Builds DCFs, LBOs, 3-statement models, and comps directly in Excel. Output
      is a working model file; staged for analyst review before use in any
      decision.
    skills: [3-statement-model, audit-xls, comps-analysis, dcf-model, lbo-model, xlsx-author]
  valuation-reviewer:
    name: Valuation Reviewer
    title: Portfolio Valuation Reviewer
    team: fund-admin-finance-ops
    description: |
      Ingests GP packages, runs the valuation template, and stages LP reporting
      with returns analysis and IC memo drafts. Staged for valuation committee
      review.
    skills: [ic-memo, portfolio-monitoring, returns-analysis, xlsx-author]
  gl-reconciler:
    name: GL Reconciler
    title: General Ledger Reconciliation Agent
    team: fund-admin-finance-ops
    description: |
      Reconciles accounts, traces the root cause of breaks, and routes packaged
      findings for sign-off. Does not post entries; every adjustment is staged
      for a controller to approve.
    skills: [audit-xls, break-trace, gl-recon, xlsx-author]
  month-end-closer:
    name: Month-End Closer
    title: Month-End Close Agent
    team: fund-admin-finance-ops
    description: |
      Runs the close checklist — accruals, roll-forwards, variance commentary —
      and prepares reports. Staged for controller review before close is signed.
    skills: [accrual-schedule, audit-xls, roll-forward, variance-commentary, xlsx-author]
  statement-auditor:
    name: Statement Auditor
    title: LP Statement Auditor
    team: fund-admin-finance-ops
    description: |
      Audits LP statements for consistency and audit-readiness — NAV tie-out,
      formatting, cross-period checks. Staged for distribution sign-off.
    skills: [audit-xls, nav-tieout, xlsx-author]
  kyc-screener:
    name: KYC Screener
    title: Client Onboarding KYC Agent
    team: operations-onboarding
    description: |
      Parses onboarding documents, runs the rules engine, and packages
      escalations with gaps flagged. Does not approve onboarding; staged for
      compliance review.
    skills: [kyc-doc-parse, kyc-rules, xlsx-author]

skills:
  3-statement-model:
    name: 3-Statement Model
    description: Build linked income statement, balance sheet, and cash flow statement.
  accrual-schedule:
    name: Accrual Schedule
    description: Build and update period-end accrual schedules.
  audit-xls:
    name: Audit XLS
    description: Audit Excel files for formula errors and consistency.
  break-trace:
    name: Break Trace
    description: Trace GL reconciliation breaks to root cause.
  client-report:
    name: Client Report
    description: Compose client briefing reports from coverage data.
  client-review:
    name: Client Review
    description: Synthesize prior interactions into a client review for meeting prep.
  competitive-analysis:
    name: Competitive Analysis
    description: Build competitive landscape analyses.
  comps-analysis:
    name: Comps Analysis
    description: Build trading-comps and precedent-transactions analyses.
  dcf-model:
    name: DCF Model
    description: Build discounted-cash-flow valuation models in Excel.
  deck-refresh:
    name: Deck Refresh
    description: Update existing pitch decks with current data.
  earnings-analysis:
    name: Earnings Analysis
    description: Analyze earnings results vs. consensus.
  earnings-preview:
    name: Earnings Preview
    description: Compose earnings preview notes ahead of release.
  gl-recon:
    name: GL Recon
    description: General-ledger reconciliation workflow.
  ib-check-deck:
    name: IB Check Deck
    description: Investment-banking deck review checklist.
  ic-memo:
    name: IC Memo
    description: Compose investment-committee memos.
  idea-generation:
    name: Idea Generation
    description: Generate investment ideas from sector research.
  investment-proposal:
    name: Investment Proposal
    description: Draft investment proposals for client meetings.
  kyc-doc-parse:
    name: KYC Doc Parse
    description: Parse onboarding documents into structured KYC fields.
  kyc-rules:
    name: KYC Rules
    description: Run the KYC rules engine over parsed onboarding data.
  lbo-model:
    name: LBO Model
    description: Build leveraged-buyout models in Excel.
  model-update:
    name: Model Update
    description: Update an existing financial model from new disclosures.
  morning-note:
    name: Morning Note
    description: Draft sell-side morning notes.
  nav-tieout:
    name: NAV Tieout
    description: Tie LP statement NAV to underlying records.
  pitch-deck:
    name: Pitch Deck
    description: Compose pitchbook decks end to end.
  portfolio-monitoring:
    name: Portfolio Monitoring
    description: Monitor portfolio company performance.
  pptx-author:
    name: PPTX Author
    description: Author and edit PowerPoint files programmatically.
  returns-analysis:
    name: Returns Analysis
    description: Compute and present fund-level returns.
  roll-forward:
    name: Roll Forward
    description: Roll balances forward across periods.
  sector-overview:
    name: Sector Overview
    description: Build industry sector overviews.
  variance-commentary:
    name: Variance Commentary
    description: Compose period-over-period variance commentary.
  xlsx-author:
    name: XLSX Author
    description: Author and edit Excel files programmatically.
```

- [ ] **Step 2: Write `LICENSE`**

Path: `claude-for-financial-services/LICENSE`. Use the standard Apache-2.0 license text. Fetch verbatim:

```bash
cd claude-for-financial-services
curl -fsSL https://www.apache.org/licenses/LICENSE-2.0.txt -o LICENSE
head -3 LICENSE
```

Expected first three lines:
```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
```

- [ ] **Step 3: Write `NOTICE`**

Path: `claude-for-financial-services/NOTICE`

```
Claude for Financial Services Agent Company Port
Copyright 2026 Jannes Stubbemann

This package is a community port into the Agent Companies format
(https://agentcompanies.io) of:

  anthropics/financial-services
  https://github.com/anthropics/financial-services
  Copyright Anthropic, PBC and contributors
  Licensed under the Apache License, Version 2.0

Skill content referenced from the upstream repository at commit
57772c3f1607229fba0270f94abf3c976bbd852f remains under the upstream
license. This package adds Agent Companies manifest scaffolding and
references upstream content by SHA; it does not modify or fork
upstream skill content.

This port is not affiliated with, endorsed by, or sponsored by Anthropic.
```

- [ ] **Step 4: Commit**

```bash
cd ~/code/paperclipai-companies
git add claude-for-financial-services/manifest.yaml \
        claude-for-financial-services/LICENSE \
        claude-for-financial-services/NOTICE
git commit -m "feat: manifest, LICENSE (Apache-2.0), NOTICE"
```

---

## Task 2: Build script — manifest loader

**Files:**
- Create: `claude-for-financial-services/scripts/build.py`
- Create: `claude-for-financial-services/tests/test_build.py`
- Create: `claude-for-financial-services/tests/fixtures/manifest_minimal.yaml`
- Create: `claude-for-financial-services/pyproject.toml`

- [ ] **Step 1: Write the failing test**

Path: `claude-for-financial-services/tests/test_build.py`

```python
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
```

Path: `claude-for-financial-services/tests/fixtures/manifest_minimal.yaml`

```yaml
schema: agentcompanies/v1
slug: test-co
name: Test Co
description: Fixture
version: 0.1.0
license: Apache-2.0
authors: [{name: Test, email: t@example.com}]
goals: [Test]
tags: [test]
upstream:
  repo: example/upstream
  commit: deadbeef
  license: Apache-2.0
affiliation: "Test"
teams:
  team-a:
    name: Team A
    description: Test team
agents:
  alpha:
    name: Alpha
    title: Alpha Agent
    team: team-a
    description: Test agent
    skills: [skill-1]
skills:
  skill-1:
    name: Skill One
    description: Test skill
```

Path: `claude-for-financial-services/pyproject.toml`

```toml
[project]
name = "claude-for-financial-services"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pyyaml>=6.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[tool.pytest.ini_options]
pythonpath = ["."]
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd ~/code/paperclipai-companies/claude-for-financial-services
pip install -e ".[dev]"
pytest tests/test_build.py::test_load_manifest_returns_structured_object -v
```

Expected: `ModuleNotFoundError: No module named 'scripts'` or `ImportError: cannot import name 'load_manifest'`.

- [ ] **Step 3a: Create `scripts/__init__.py` (empty)**

Path: `claude-for-financial-services/scripts/__init__.py` — empty file. This makes `scripts/` an importable package so `from scripts.build import …` works from `scripts/check.py` and from pytest.

```bash
touch claude-for-financial-services/scripts/__init__.py
```

- [ ] **Step 3b: Write the minimal implementation**

Path: `claude-for-financial-services/scripts/build.py`

```python
"""Build script for the Claude for Financial Services Agent Company package.

Generates COMPANY.md, TEAM.md, AGENTS.md, SKILL.md files plus the org-chart
image from the canonical manifest.yaml.
"""
from __future__ import annotations

from dataclasses import dataclass, field
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


if __name__ == "__main__":
    m = load_manifest(ROOT / "manifest.yaml")
    print(f"Loaded manifest: {m.slug} ({len(m.agents)} agents, {len(m.skills)} skills)")
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_load_manifest_returns_structured_object -v
```

Expected: `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py \
        claude-for-financial-services/tests/fixtures/manifest_minimal.yaml \
        claude-for-financial-services/pyproject.toml
git commit -m "feat(build): manifest loader with dataclass schema"
```

---

## Task 3: Build script — canonical upstream skill paths

The skill graph from the spec lists which upstream agents own each skill. For shared skills, we resolve a canonical path: most-recent upstream commit touching the file; alphabetical agent name as tiebreak.

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py` (add `resolve_canonical_paths`)
- Modify: `claude-for-financial-services/tests/test_build.py` (add test)

- [ ] **Step 1: Write the failing test**

Append to `claude-for-financial-services/tests/test_build.py`:

```python
from scripts.build import resolve_canonical_paths


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
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_resolve_canonical_paths_picks_alphabetical_when_dates_equal -v
```

Expected: `ImportError: cannot import name 'resolve_canonical_paths'`.

- [ ] **Step 3: Add the implementation to `scripts/build.py`**

Append after `load_manifest`:

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_resolve_canonical_paths_picks_alphabetical_when_dates_equal -v
```

Expected: `PASSED`.

- [ ] **Step 5: Add a tiny helper that fetches real `file_dates` from the upstream repo**

Append to `scripts/build.py`:

```python
import json
import subprocess


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
```

- [ ] **Step 6: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py
git commit -m "feat(build): canonical upstream-path resolution for shared skills"
```

---

## Task 4: Build script — content hashes

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py`
- Modify: `claude-for-financial-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_build.py`:

```python
from scripts.build import compute_content_hash


def test_compute_content_hash_is_sha256_hex():
    content = b"hello world"
    h = compute_content_hash(content)
    # `sha256("hello world")` = b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
    assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_compute_content_hash_is_sha256_hex -v
```

Expected: `ImportError: cannot import name 'compute_content_hash'`.

- [ ] **Step 3: Add implementation**

Append to `scripts/build.py`:

```python
import hashlib


def compute_content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fetch_upstream_file(repo: str, commit: str, path: str) -> bytes:
    """Fetch raw bytes of a file from upstream at the pinned commit."""
    import base64
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={commit}", "--jq", ".content"],
        check=True, capture_output=True, text=True,
    )
    return base64.b64decode(out.stdout.strip())
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_compute_content_hash_is_sha256_hex -v
```

Expected: `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py
git commit -m "feat(build): content-hash + upstream-file-fetch helpers"
```

---

## Task 5: Build script — emit COMPANY.md

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py`
- Modify: `claude-for-financial-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_build.py`:

```python
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
    assert fm["kind"] == "company"
    assert fm["slug"] == "test-co"
    assert fm["license"] == "Apache-2.0"
    assert fm["metadata"]["upstream"]["commit"] == "deadbeef"
    body = text[fm_end + len("\n---\n"):]
    assert "Test Co" in body
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_emit_company_produces_valid_yaml_frontmatter -v
```

Expected: `ImportError: cannot import name 'emit_company'`.

- [ ] **Step 3: Add implementation**

Append to `scripts/build.py`:

```python
def _frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"


def emit_company(m: Manifest, out_path: Path) -> None:
    fm = {
        "schema": m.schema,
        "kind": "company",
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_emit_company_produces_valid_yaml_frontmatter -v
```

Expected: `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py
git commit -m "feat(build): emit COMPANY.md from manifest"
```

---

## Task 6: Build script — emit TEAM.md

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py`
- Modify: `claude-for-financial-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_build.py`:

```python
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
    assert fm["kind"] == "team"
    assert fm["slug"] == "team-a"
    assert fm["includes"] == ["../../agents/alpha/AGENTS.md"]
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_emit_teams_creates_one_file_per_team -v
```

Expected: `ImportError: cannot import name 'emit_teams'`.

- [ ] **Step 3: Add implementation**

Append to `scripts/build.py`:

```python
def emit_teams(m: Manifest, teams_root: Path) -> None:
    # Build team -> [agent_slug] mapping from agents
    team_agents: dict[str, list[str]] = {t: [] for t in m.teams}
    for agent_slug, agent in m.agents.items():
        team_agents[agent.team].append(agent_slug)

    for slug, team in m.teams.items():
        out_dir = teams_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "kind": "team",
            "slug": slug,
            "name": team.name,
            "description": team.description,
            "includes": [
                f"../../agents/{a}/AGENTS.md" for a in sorted(team_agents[slug])
            ],
        }
        body = f"\n# {team.name}\n\n{team.description}\n"
        (out_dir / "TEAM.md").write_text(_frontmatter(fm) + body)
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_emit_teams_creates_one_file_per_team -v
```

Expected: `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py
git commit -m "feat(build): emit TEAM.md from manifest"
```

---

## Task 7: Build script — emit AGENTS.md

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py`
- Modify: `claude-for-financial-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_build.py`:

```python
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
    assert fm["kind"] == "agent"
    assert fm["slug"] == "alpha"
    assert fm["title"] == "Alpha Agent"
    assert fm["reportsTo"] == "../../teams/team-a/TEAM.md"
    assert fm["skills"] == ["skill-1"]
    assert fm["metadata"]["sources"][0]["url"] == \
        "https://github.com/example/upstream/tree/deadbeef/plugins/agent-plugins/alpha"

    body = text[fm_end + len("\n---\n"):]
    assert "Test agent" in body
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_emit_agents_creates_one_file_per_agent_with_skill_list -v
```

Expected: `ImportError: cannot import name 'emit_agents'`.

- [ ] **Step 3: Add implementation**

Append to `scripts/build.py`:

```python
def emit_agents(m: Manifest, agents_root: Path) -> None:
    for slug, agent in m.agents.items():
        out_dir = agents_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "kind": "agent",
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_emit_agents_creates_one_file_per_agent_with_skill_list -v
```

Expected: `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py
git commit -m "feat(build): emit AGENTS.md from manifest"
```

---

## Task 8: Build script — emit SKILL.md

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py`
- Modify: `claude-for-financial-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_build.py`:

```python
from scripts.build import emit_skills


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
    assert fm["kind"] == "skill"
    assert fm["slug"] == "skill-1"
    src = fm["metadata"]["sources"][0]
    assert src["repo"] == "example/upstream"
    assert src["commit"] == "deadbeef"
    assert src["path"] == "plugins/agent-plugins/alpha/skills/skill-1/SKILL.md"
    assert src["mode"] == "referenced"
    assert src["contentHash"] == "abc123"
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_emit_skills_creates_one_file_per_skill_with_canonical_path -v
```

Expected: `ImportError: cannot import name 'emit_skills'`.

- [ ] **Step 3: Add implementation**

Append to `scripts/build.py`:

```python
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
            "kind": "skill",
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_emit_skills_creates_one_file_per_skill_with_canonical_path -v
```

Expected: `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py
git commit -m "feat(build): emit SKILL.md from manifest"
```

---

## Task 9: Build script — `main()` and org-chart image

**Files:**
- Modify: `claude-for-financial-services/scripts/build.py`
- Modify: `claude-for-financial-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_build.py`:

```python
from scripts.build import emit_org_chart_dot


def test_emit_org_chart_dot_contains_all_agents_and_teams():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    dot = emit_org_chart_dot(m)
    assert "digraph" in dot
    assert '"team-a"' in dot
    assert '"alpha"' in dot
    assert '"team-a" -> "alpha"' in dot
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_build.py::test_emit_org_chart_dot_contains_all_agents_and_teams -v
```

Expected: `ImportError: cannot import name 'emit_org_chart_dot'`.

- [ ] **Step 3: Add implementation**

Append to `scripts/build.py`:

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_build.py::test_emit_org_chart_dot_contains_all_agents_and_teams -v
```

Expected: `PASSED`.

- [ ] **Step 5: Run the full build end-to-end**

```bash
which dot >/dev/null || brew install graphviz
python -m scripts.build
ls COMPANY.md teams/coverage-advisory/TEAM.md agents/pitch-agent/AGENTS.md skills/dcf-model/SKILL.md images/org-chart.png
```

Expected: all files exist, build script prints "Build complete."

- [ ] **Step 6: Commit**

```bash
git add claude-for-financial-services/scripts/build.py \
        claude-for-financial-services/tests/test_build.py \
        claude-for-financial-services/COMPANY.md \
        claude-for-financial-services/teams/ \
        claude-for-financial-services/agents/ \
        claude-for-financial-services/skills/ \
        claude-for-financial-services/images/
git commit -m "feat(build): main() generates 46 manifests + org-chart image"
```

---

## Task 10: Check script — schema validation

**Files:**
- Create: `claude-for-financial-services/scripts/check.py`
- Create: `claude-for-financial-services/tests/test_check.py`

- [ ] **Step 1: Write the failing test**

Path: `claude-for-financial-services/tests/test_check.py`

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_check.py -v
```

Expected: `ModuleNotFoundError` for `scripts.check`.

- [ ] **Step 3: Add implementation**

Path: `claude-for-financial-services/scripts/check.py`

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_check.py -v
```

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/check.py \
        claude-for-financial-services/tests/test_check.py
git commit -m "feat(check): frontmatter schema validation"
```

---

## Task 11: Check script — cross-reference resolution

**Files:**
- Modify: `claude-for-financial-services/scripts/check.py`
- Modify: `claude-for-financial-services/tests/test_check.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_check.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_check.py -v -k cross
```

Expected: ImportError on `check_cross_references`.

- [ ] **Step 3: Add implementation**

Append to `scripts/check.py`:

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_check.py -v -k cross
```

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add claude-for-financial-services/scripts/check.py \
        claude-for-financial-services/tests/test_check.py
git commit -m "feat(check): cross-reference resolution for agent→skill"
```

---

## Task 12: Check script — content-hash freshness

**Files:**
- Modify: `claude-for-financial-services/scripts/check.py`
- Modify: `claude-for-financial-services/tests/test_check.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_check.py`:

```python
from scripts.check import check_content_hashes


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
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
pytest tests/test_check.py -v -k content_hashes
```

Expected: ImportError on `check_content_hashes`.

- [ ] **Step 3: Add implementation**

Append to `scripts/check.py`:

```python
import hashlib
from scripts.build import fetch_upstream_file  # reuse


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_content_hashes(package_root: Path) -> None:
    skills_dir = package_root / "skills"
    if not skills_dir.exists():
        return
    for skill_md in skills_dir.glob("*/SKILL.md"):
        fm = parse_frontmatter(skill_md.read_text())
        sources = fm.get("metadata", {}).get("sources", [])
        for src in sources:
            if src.get("mode") != "referenced":
                continue
            actual = _sha256(fetch_upstream_file(src["repo"], src["commit"], src["path"]))
            expected = src.get("contentHash")
            if actual != expected:
                raise ValidationError(
                    f"{skill_md.relative_to(package_root)}: contentHash {expected!r} "
                    f"does not match upstream sha256 {actual!r} at {src['path']}"
                )


def main() -> int:
    """Run all checks. Exits 0 on success, 1 on first ValidationError."""
    try:
        # 1. Schema validation across every manifest
        for kind, glob in [
            ("company", "COMPANY.md"),
            ("team", "teams/*/TEAM.md"),
            ("agent", "agents/*/AGENTS.md"),
            ("skill", "skills/*/SKILL.md"),
        ]:
            for path in ROOT.glob(glob):
                fm = parse_frontmatter(path.read_text())
                validate_frontmatter(kind, fm)

        # 2. Cross-references
        check_cross_references(ROOT)

        # 3. Content-hash freshness (network — slow)
        check_content_hashes(ROOT)

    except ValidationError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("OK: schema, cross-references, content hashes all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_check.py -v
```

Expected: all 5 tests pass.

- [ ] **Step 5: Run check.py end-to-end against the real package**

```bash
cd ~/code/paperclipai-companies/claude-for-financial-services
python -m scripts.check
```

Expected: `OK: schema, cross-references, content hashes all valid.` (network-bound; takes 10–30s for 31 upstream fetches.)

- [ ] **Step 6: Commit**

```bash
git add claude-for-financial-services/scripts/check.py \
        claude-for-financial-services/tests/test_check.py
git commit -m "feat(check): content-hash freshness via upstream re-fetch"
```

---

## Task 13: Makefile

**Files:**
- Create: `claude-for-financial-services/Makefile`

- [ ] **Step 1: Write the Makefile**

Path: `claude-for-financial-services/Makefile`

```make
.PHONY: build check test bump clean

build:
	python -m scripts.build

check:
	python -m scripts.check

test:
	pytest -v

# Update the upstream SHA pin in manifest.yaml, then rebuild + recheck.
# Usage: make bump SHA=<new-sha>
bump:
	@test -n "$(SHA)" || (echo "ERROR: pass SHA=<new-sha>" >&2; exit 1)
	sed -i.bak -E 's/^( {2}commit: ).*/\1$(SHA)/' manifest.yaml
	rm manifest.yaml.bak
	$(MAKE) build
	$(MAKE) check

clean:
	rm -rf COMPANY.md teams/ agents/ skills/ images/
```

- [ ] **Step 2: Verify `make build` and `make check` work**

```bash
cd ~/code/paperclipai-companies/claude-for-financial-services
make clean
make build
make check
make test
```

Expected: all four targets succeed.

- [ ] **Step 3: Commit**

```bash
git add claude-for-financial-services/Makefile
git commit -m "build: Makefile with build/check/test/bump/clean targets"
```

---

## Task 14: README.md

**Files:**
- Create: `claude-for-financial-services/README.md`

- [ ] **Step 1: Write the README**

Path: `claude-for-financial-services/README.md` (the outer fence below uses **four** backticks because the README itself contains three-backtick code blocks):

````markdown
# Claude for Financial Services

> **Community port** of [`anthropics/financial-services`](https://github.com/anthropics/financial-services) into the [Agent Companies](https://agentcompanies.io) format. **Not affiliated with or endorsed by Anthropic.**

10 agents across 4 functional areas — coverage & advisory, research & modeling, fund admin & finance ops, operations & onboarding. Skills are referenced upstream by pinned commit SHA, not vendored.

## Install

```bash
npx companies.sh add paperclipai/companies/claude-for-financial-services
```

## Org chart

![Org chart](./images/org-chart.png)

## Agents

| Agent | Team | What it does | Skills |
|---|---|---|---|
| **Pitch Agent** | Coverage & Advisory | Comps, precedents, LBO → branded pitch deck, end to end | 11 |
| **Meeting Prep Agent** | Coverage & Advisory | Briefing pack before every client meeting | 4 |
| **Market Researcher** | Research & Modeling | Sector or theme → industry overview, competitive landscape, peer comps, ideas shortlist | 5 |
| **Earnings Reviewer** | Research & Modeling | Earnings call + filings → model update → note draft | 6 |
| **Model Builder** | Research & Modeling | DCF, LBO, 3-statement, comps — live in Excel | 6 |
| **Valuation Reviewer** | Fund Admin & Finance Ops | Ingests GP packages, runs valuation template, stages LP reporting | 4 |
| **GL Reconciler** | Fund Admin & Finance Ops | Finds breaks, traces root cause, routes for sign-off | 4 |
| **Month-End Closer** | Fund Admin & Finance Ops | Accruals, roll-forwards, variance commentary | 5 |
| **Statement Auditor** | Fund Admin & Finance Ops | Audits LP statements before distribution | 3 |
| **KYC Screener** | Operations & Onboarding | Parses onboarding docs, runs the rules engine, flags gaps | 3 |

## Skills (31 unique, referenced upstream)

Most-shared: `xlsx-author` (8 agents) · `audit-xls` (6) · `pptx-author` (3) · `comps-analysis` (3).

Each `skills/<slug>/SKILL.md` file is a thin reference manifest pointing to the upstream file at the pinned commit. Skill content is fetched on demand by the runtime; nothing is forked or vendored.

## Boundaries

Nothing in this package constitutes investment, legal, tax, or accounting advice. These agents draft analyst work product (models, memos, research notes, reconciliations) for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding; every output is staged for human sign-off. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your firm.

## Provenance

| Field | Value |
|---|---|
| Upstream | [`anthropics/financial-services`](https://github.com/anthropics/financial-services) |
| Pinned commit | `57772c3f1607229fba0270f94abf3c976bbd852f` (2026-05-07) |
| Upstream license | Apache-2.0 |
| Port license | Apache-2.0 (matches upstream) |

See [`NOTICE`](./NOTICE) for full attribution.

## Maintenance — bumping the upstream SHA

```bash
make bump SHA=<new-upstream-sha>
make test
git diff --stat
git commit -am "chore: bump upstream to <short-sha>"
```

`make bump` rewrites `manifest.yaml`, regenerates all 46 manifests, refetches content hashes, and runs `make check`. If any upstream file's content hash has changed, the regenerated SKILL.md reflects it.

## Layout

```
claude-for-financial-services/
├── COMPANY.md                  # generated
├── teams/<slug>/TEAM.md        # generated, ×4
├── agents/<slug>/AGENTS.md     # generated, ×10
├── skills/<slug>/SKILL.md      # generated, ×31
├── manifest.yaml               # canonical source — edit this, run `make build`
├── scripts/build.py            # manifest generator
├── scripts/check.py            # validator
├── Makefile
├── images/org-chart.png        # generated
├── tests/                      # pytest unit tests for the generator
├── docs/superpowers/           # design spec + implementation plan
├── LICENSE                     # Apache-2.0
└── NOTICE                      # upstream attribution
```

## Spec & implementation plan

- Design: [`docs/superpowers/specs/2026-05-09-agent-company-port-design.md`](./docs/superpowers/specs/2026-05-09-agent-company-port-design.md)
- Plan: [`docs/superpowers/plans/2026-05-09-agent-company-port-implementation.md`](./docs/superpowers/plans/2026-05-09-agent-company-port-implementation.md)
````

- [ ] **Step 2: Sanity-check the README**

```bash
cd ~/code/paperclipai-companies/claude-for-financial-services
grep -q "Community port" README.md
grep -q "Not affiliated" README.md
grep -q "npx companies.sh add" README.md
grep -q "Apache-2.0" README.md
grep -q "57772c3f" README.md
```

Expected: all five `grep -q` succeed (exit 0).

- [ ] **Step 3: Commit**

```bash
git add claude-for-financial-services/README.md
git commit -m "docs: README with attribution, install, agents/skills tables"
```

---

## Task 15: Add row to catalog root README

**Files:**
- Modify: `~/code/paperclipai-companies/README.md` (catalog root)

- [ ] **Step 1: Inspect the existing Table of Contents**

```bash
cd ~/code/paperclipai-companies
grep -n "^| " README.md | head -20
```

Expected: rows for `GStack`, `Superpowers Dev Shop`, `Agency Agents`, etc.

- [ ] **Step 2: Add the new row in alphabetical position**

Insert this row in the catalog's main "Companies" table (alphabetical by display name; goes after "Agency Agents" and before "Aeon Intelligence" if alphabetized strictly, or wherever the existing convention places it — match neighbouring entries):

```markdown
| [Claude for Financial Services](#claude-for-financial-services) | 10     | 31     | [financial-services](https://github.com/anthropics/financial-services)             |
```

Then add a section in the "Companies" body, mirroring the format used for `superpowers` and `gstack`:

````markdown
### [Claude for Financial Services](./claude-for-financial-services)

```bash
npx companies.sh add paperclipai/companies/claude-for-financial-services
```

A finance company spanning coverage & advisory, research & modeling, fund admin & finance ops, and operations & onboarding. Community port of [anthropics/financial-services](https://github.com/anthropics/financial-services) — not affiliated with Anthropic.

![Claude for Financial Services Org Chart](./claude-for-financial-services/images/org-chart.png)

> **Agents (10):** Pitch Agent, Meeting Prep Agent, Market Researcher, Earnings Reviewer, Model Builder, Valuation Reviewer, GL Reconciler, Month-End Closer, Statement Auditor, KYC Screener
>
> **Skills (31):** 3-statement-model, accrual-schedule, audit-xls, break-trace, client-report, client-review, competitive-analysis, comps-analysis, dcf-model, deck-refresh, earnings-analysis, earnings-preview, gl-recon, ib-check-deck, ic-memo, idea-generation, investment-proposal, kyc-doc-parse, kyc-rules, lbo-model, model-update, morning-note, nav-tieout, pitch-deck, portfolio-monitoring, pptx-author, returns-analysis, roll-forward, sector-overview, variance-commentary, xlsx-author
````

- [ ] **Step 3: Verify both edits applied**

```bash
grep -c "claude-for-financial-services" README.md
```

Expected: ≥ 3 (one in TOC table, one in section heading, at least one in body).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs(catalog): add Claude for Financial Services to TOC and body"
```

---

## Task 16: Catalog dry-run validation

**Files:** none (verification only)

- [ ] **Step 1: Run the catalog's own validator (Paperclip dry-run)**

```bash
cd ~/code/paperclipai-companies
npx --yes paperclipai company import --from ./claude-for-financial-services --dry-run
```

Expected: exits 0; prints discovered company structure (10 agents, 31 skills). If `npx paperclipai` is not yet released, fall back to whatever the current Paperclip CLI is — check the catalog's CONTRIBUTING.md for the latest invocation.

- [ ] **Step 2: Re-run our local checks for completeness**

```bash
cd claude-for-financial-services
make test
make check
```

Expected: pytest 100% passing; `check.py` prints `OK: schema, cross-references, content hashes all valid.`

- [ ] **Step 3: Sanity-check the diff size**

```bash
cd ~/code/paperclipai-companies
git log --oneline upstream/master..HEAD
git diff --stat upstream/master..HEAD | tail -1
```

Expected: ~14 commits on the branch; diff totals roughly 50–60 changed files (46 manifests + scripts + docs + 2 images).

- [ ] **Step 4: No commit (verification only — but if you tweaked anything, commit it)**

---

## Task 17: Open the PR

**Files:** none (GitHub-only)

- [ ] **Step 1: Push the branch to your fork**

```bash
cd ~/code/paperclipai-companies
git push -u origin add-claude-for-financial-services
```

Expected: branch published.

- [ ] **Step 2: Open the PR**

```bash
gh pr create \
  --repo paperclipai/companies \
  --title "Add Claude for Financial Services (community port of anthropics/financial-services)" \
  --body "$(cat <<'EOF'
## Summary

Adds `claude-for-financial-services/` — a community port of [`anthropics/financial-services@57772c3f`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f) into the Agent Companies format.

- **10 agents** across 4 functional areas: coverage & advisory, research & modeling, fund admin & finance ops, operations & onboarding.
- **31 unique skills**, all referenced upstream by pinned commit SHA. Nothing is vendored or forked.
- **License:** Apache-2.0 (matches upstream); `NOTICE` preserves upstream attribution per Apache-2.0 §4.

## Why

No finance-domain entry currently in the catalog. The format ports cleanly because `anthropics/financial-services` already uses the Agent Skills `SKILL.md` format — this PR adds Agent Companies scaffolding (COMPANY.md, TEAM.md, AGENTS.md) around the existing skill graph and de-duplicates shared skills (e.g. `xlsx-author` is referenced by 8 of 10 upstream agents).

## Attribution

**Community port. Not affiliated with or endorsed by Anthropic.** Author: Jannes Stubbemann <jannes@aqora.io>.

The `affiliation:` line in `COMPANY.md` and the README header both make this explicit. Happy to add a "Community ports" subsection to the catalog README if maintainers want to visually separate self-published from community-ported entries.

## Validation

- `make test` ✓ (pytest unit tests on the build/check scripts)
- `make check` ✓ (schema, cross-references, content-hash freshness against upstream)
- `paperclipai company import --from . --dry-run` ✓

## Open questions for reviewers

- **Skill layout.** I put SKILL.md files at the company root (`skills/<slug>/SKILL.md`) and dedup. Upstream uses per-agent skill directories with duplicates. Mirroring upstream would mean 51 SKILL.md files instead of 31; I went with dedup because shared skills are a first-class Agent Companies concept. Happy to switch if maintainers prefer mirroring.
- **Endorsement framing.** Anything you'd like changed in the README header / `affiliation:` to make the community-port status clearer to downstream users?

## Maintenance

`make bump SHA=<new-sha>` rewrites `manifest.yaml`, regenerates all 46 manifests, refetches and rehashes upstream content. First-pass cadence: bump on upstream release tags or every ~4 weeks if untagged.

## Spec & plan

- Design: [`docs/superpowers/specs/2026-05-09-agent-company-port-design.md`](./claude-for-financial-services/docs/superpowers/specs/2026-05-09-agent-company-port-design.md)
- Plan: [`docs/superpowers/plans/2026-05-09-agent-company-port-implementation.md`](./claude-for-financial-services/docs/superpowers/plans/2026-05-09-agent-company-port-implementation.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: `gh` prints the PR URL.

- [ ] **Step 3: Verify the PR**

```bash
gh pr view --repo paperclipai/companies --web
```

Expected: PR opens in your browser. Manually skim that:
- The diff includes only `claude-for-financial-services/` and the catalog `README.md` edit.
- All 46 manifests are present.
- The org-chart image renders.
- CI (if any) starts running.

- [ ] **Step 4: Done**

Capture the PR URL and report it back. Implementation complete.

---

## Self-Review

Spec coverage check (each section in the design doc → which task implements it):

| Spec section | Implemented in |
|---|---|
| Goal & boundaries | Task 1 (manifest goals + COMPANY.md body in Task 5) |
| Architecture / file layout | Task 0 (dir setup) + Tasks 5–9 (generated files) |
| Manifest generation rationale | Tasks 2–9 (build script with TDD) |
| COMPANY.md / TEAM.md / AGENTS.md / SKILL.md frontmatter shapes | Tasks 5, 6, 7, 8 respectively |
| Skill graph (51 edges → 31 unique) | Task 1 (manifest.yaml encodes both sides; agents.skills + skills dict) |
| Canonical upstream-path resolution | Task 3 |
| Pinned commit SHA | Task 1 (`upstream.commit` field) |
| Apache-2.0 license + NOTICE | Task 1 |
| Validation (schema / cross-ref / content hash) | Tasks 10, 11, 12 respectively |
| `make check` Makefile target | Task 13 |
| `paperclipai company import --dry-run` gate | Task 16 step 1 |
| README structure (8 sections from spec) | Task 14 |
| Catalog root README edit | Task 15 |
| PR description template | Task 17 step 2 |
| Risks (endorsement perception, churn, maintainer pushback, NOTICE compliance) | Surfaced in PR body (Task 17) and README boundaries section (Task 14) |
| Maintenance cadence (`make bump`) | Task 13 (Makefile target) + Task 14 (README §maintenance) |

No gaps detected.

Type consistency spot-checks:
- `Manifest` dataclass fields used identically across Tasks 2–9 ✓
- `validate_frontmatter(kind, fm)` signature stable across Tasks 10–12 ✓
- `fetch_upstream_file(repo, commit, path) -> bytes` signature stable across Tasks 4 (definition), 9 (use in build main), 12 (use in check) ✓
- Skill slug naming consistent across `manifest.yaml`, agent `skills:` lists, and `skills/<slug>/` dirs ✓

No placeholders found. Plan is executable as-written.
