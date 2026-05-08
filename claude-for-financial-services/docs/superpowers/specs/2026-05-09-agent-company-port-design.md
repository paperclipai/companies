# Claude for Financial Services — Agent Companies Port Design

- **Date:** 2026-05-09
- **Author:** Jannes Stubbemann <jannes@aqora.io>
- **Status:** Design — pending implementation
- **Source:** `anthropics/financial-services` @ commit `57772c3f1607229fba0270f94abf3c976bbd852f` (2026-05-07), Apache-2.0
- **Target:** `paperclipai/companies` catalog (PR), `agentcompanies/v1` schema

## Goal

Port Anthropic's `anthropics/financial-services` reference agents into the [Agent Companies](https://agentcompanies.io/specification) format and submit a single PR adding a new top-level company `claude-for-financial-services/` to the [`paperclipai/companies`](https://github.com/paperclipai/companies) catalog.

## Non-goals

- Adding aqora-specific extensions, branding, or runtime config.
- Modifying the upstream skill content. We reference, we do not fork.
- Building runtime support — this is a static package; the runtime is Paperclip's.
- Endorsement from or coordination with Anthropic. This is explicitly a community port.

## Boundaries (lifted from upstream, preserved here)

Nothing in this package constitutes investment, legal, tax, or accounting advice. The agents draft analyst work product (models, memos, research notes, reconciliations) for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding. Every output is staged for human sign-off.

## Architecture

Single top-level directory inside a fork of `paperclipai/companies`, following the catalog's `CONTRIBUTING.md` plus the optional `teams/` directory.

```
claude-for-financial-services/
├── COMPANY.md
├── README.md
├── LICENSE                            # Apache-2.0, matches upstream
├── NOTICE                             # preserves upstream attribution
├── manifest.yaml                      # canonical source — agents, teams, skills, SHA
├── Makefile                           # `make build` `make check`
├── scripts/
│   └── build.py                       # generates manifests + org chart
├── images/
│   └── org-chart.png                  # generated
├── teams/
│   ├── coverage-advisory/TEAM.md
│   ├── research-modeling/TEAM.md
│   ├── fund-admin-finance-ops/TEAM.md
│   └── operations-onboarding/TEAM.md
├── agents/                            # 10 directories, one AGENTS.md each
│   └── <agent-slug>/AGENTS.md
├── skills/                            # 31 directories, one SKILL.md each
│   └── <skill-slug>/SKILL.md
└── docs/superpowers/specs/
    └── 2026-05-09-agent-company-port-design.md   # this file
```

### Why skills at the company root, not under each agent

Agent Companies treats skills as reusable. `xlsx-author` is referenced by 8 of 10 upstream agents; mirroring upstream's per-agent layout would write 8 nearly-identical SKILL.md files. A single `skills/xlsx-author/SKILL.md` resolved by slug from each `AGENTS.md.skills:` entry is cleaner and matches the resolution semantics described in the spec.

### Why manifests are generated, not hand-written

46 manifests (1 COMPANY + 4 TEAM + 10 AGENTS + 31 SKILL) is too many to keep coherent through SHA bumps. A single `manifest.yaml` lists the canonical structure; `scripts/build.py` produces every YAML file. Hand-edits to generated files fail `make check`. This matches the convention used by other catalog entries that reference upstream skills (e.g. `superpowers`).

## Manifest specifications

### COMPANY.md

```yaml
---
schema: agentcompanies/v1
kind: company
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
  - Cover the four FSI workflow areas Anthropic shipped: coverage & advisory, research & modeling, fund admin & finance ops, operations & onboarding.
  - Stage every output for human sign-off — no agent here executes trades, posts to a ledger, or approves onboarding.
tags: [finance, fsi, investment-banking, equity-research, private-equity, fund-admin, kyc]
metadata:
  upstream:
    repo: anthropics/financial-services
    commit: 57772c3f1607229fba0270f94abf3c976bbd852f
    license: Apache-2.0
  affiliation: "Community port. Not affiliated with or endorsed by Anthropic."
---
```

Body: full upstream disclaimer verbatim, plus a one-line description of each of the four teams.

### TEAM.md (×4)

```yaml
---
kind: team
slug: <team-slug>
name: <human name>
description: <one line>
includes:
  - ../../agents/<agent-1>/AGENTS.md
  - ../../agents/<agent-2>/AGENTS.md
---
```

Bodies: 1–2 sentences per team.

### AGENTS.md (×10)

```yaml
---
kind: agent
slug: <agent-slug>
name: <human name>
title: <role title>
reportsTo: ../../teams/<team>/TEAM.md
skills: [<slug>, <slug>, ...]
tags: [...]
metadata:
  sources:
    - url: https://github.com/anthropics/financial-services/tree/<SHA>/plugins/agent-plugins/<slug>
      mode: referenced
---

# <Agent Name>

<2–4 sentence role description, condensed from the upstream agent. Always
ends with the "stages output for human review" boundary.>
```

Body length is short (2–4 sentences). The spec says *"the markdown body is the canonical default instruction content for the role"*; long procedural instructions belong in skills, not in agent bodies.

### SKILL.md (×31)

```yaml
---
kind: skill
slug: <skill-slug>
name: <human name>
description: <one-line description for skill discovery>
version: 0.1.0
metadata:
  sources:
    - repo: anthropics/financial-services
      commit: 57772c3f1607229fba0270f94abf3c976bbd852f
      path: plugins/agent-plugins/<canonical-owner>/skills/<skill-slug>/SKILL.md
      mode: referenced
      contentHash: <sha256 of upstream file at the pinned SHA>
---

> Skill content lives upstream at the path above (commit `<SHA>`). Pull the
> upstream file before invocation; do not edit this manifest in place.
```

Body is intentionally a stub.

## Skill graph (51 edges → 31 unique skills)

| Agent | Team | Skills |
|---|---|---|
| pitch-agent | coverage-advisory | 3-statement-model, audit-xls, comps-analysis, dcf-model, deck-refresh, ib-check-deck, lbo-model, pitch-deck, pptx-author, sector-overview, xlsx-author |
| meeting-prep-agent | coverage-advisory | client-report, client-review, investment-proposal, pptx-author |
| market-researcher | research-modeling | competitive-analysis, comps-analysis, idea-generation, pptx-author, sector-overview |
| earnings-reviewer | research-modeling | audit-xls, earnings-analysis, earnings-preview, model-update, morning-note, xlsx-author |
| model-builder | research-modeling | 3-statement-model, audit-xls, comps-analysis, dcf-model, lbo-model, xlsx-author |
| valuation-reviewer | fund-admin-finance-ops | ic-memo, portfolio-monitoring, returns-analysis, xlsx-author |
| gl-reconciler | fund-admin-finance-ops | audit-xls, break-trace, gl-recon, xlsx-author |
| month-end-closer | fund-admin-finance-ops | accrual-schedule, audit-xls, roll-forward, variance-commentary, xlsx-author |
| statement-auditor | fund-admin-finance-ops | audit-xls, nav-tieout, xlsx-author |
| kyc-screener | operations-onboarding | kyc-doc-parse, kyc-rules, xlsx-author |

Most-shared skills (dedup wins): `xlsx-author` × 8, `audit-xls` × 6, `pptx-author` × 3, `comps-analysis` × 3, `sector-overview` × 2, `dcf-model` × 2, `lbo-model` × 2, `3-statement-model` × 2.

### Canonical upstream paths for shared skills

For skills that exist under multiple upstream agent directories, the canonical `metadata.sources[0].path` is chosen mechanically by `scripts/build.py`:

1. Pick the upstream copy with the most recent commit touching it.
2. If equal, pick alphabetical agent name.

The choice is recorded in `manifest.yaml` and reflected in the generated SKILL.md. Reviewers shouldn't need to know which copy was chosen unless they're auditing.

## Validation

`make check` runs three local checks:

1. **Frontmatter schema validation.** Every manifest has the required fields for its `kind`. Catches typos, missing fields, kind/filename mismatch.
2. **Cross-reference resolution.** Every `skills:` entry resolves to a real `skills/<slug>/SKILL.md`. Every `reportsTo:` and `includes:` resolves. Every `metadata.sources[].path` exists in the upstream repo at the pinned SHA (verified via `gh api`).
3. **Content hash freshness.** For each `SKILL.md.metadata.sources[0].contentHash`, fetch the upstream file at the pinned SHA, hash, compare. Stale hashes fail the build.

Catalog gate: `paperclipai company import --from . --dry-run` must exit 0 before opening the PR.

## README.md outline

1. One-paragraph intro with attribution: *"Community port of `anthropics/financial-services`. Not affiliated with or endorsed by Anthropic."*
2. Import command: `npx companies.sh add paperclipai/companies/claude-for-financial-services`.
3. Org-chart image (`./images/org-chart.png`).
4. Agents table (10 rows).
5. Skills table (31 rows).
6. Boundaries section — full upstream disclaimer verbatim.
7. Provenance — pinned upstream SHA, license, NOTICE.
8. Maintenance — how to bump SHA: edit `manifest.yaml`, `make build`, `make check`, `paperclipai company import --dry-run`, commit.

## PR submission plan

1. Fork `paperclipai/companies` to `<your-gh>/companies`. Clone to `~/code/paperclipai-companies/`.
2. Branch: `add-claude-for-financial-services`.
3. Move/copy the generated package into `claude-for-financial-services/` at the catalog root.
4. Add a row to the catalog's root `README.md` Table of Contents alongside the existing entries (`gstack`, `superpowers`, etc.).
5. Run `make check` and `paperclipai company import --dry-run`. Both must pass.
6. Open PR with the description template below.

### PR description template

- **Summary:** Adds `claude-for-financial-services/` — a community port of `anthropics/financial-services@57772c3f` into Agent Companies format. 10 agents, 4 teams, 31 skills referenced upstream.
- **Why:** No finance-domain entry currently in the catalog. The format ports cleanly because upstream already uses SKILL.md.
- **Attribution:** Community port. Not affiliated with or endorsed by Anthropic. Author: Jannes Stubbemann <jannes@aqora.io>. Upstream license preserved (Apache-2.0); NOTICE file included.
- **Validation:** `make check` ✓ · `paperclipai company import --dry-run` ✓
- **Open questions for reviewers:** Whether the skill-at-root layout is the right call vs. mirroring upstream per-agent dirs; whether to land now or wait for Anthropic acknowledgment; whether the catalog README should grow a "Community ports" section visually distinct from self-published entries.

## Risks

- **Endorsement perception.** Reviewers and downstream users may misread this as Anthropic-published. Mitigation: explicit `affiliation:` line in `COMPANY.md`, prominent attribution in README header, PR description spelling it out.
- **Upstream churn.** `anthropics/financial-services` is actively developed (commit from 2 days ago). Without bump cadence, the port goes stale. Mitigation: documented bump process in README §8; first-pass cadence is "bump on upstream release tags or every ~4 weeks."
- **Catalog maintainer pushback.** Maintainers may prefer per-agent skill directories to mirror upstream more literally. Mitigation: PR description explicitly invites this feedback rather than asserting correctness.
- **Apache-2.0 NOTICE compliance.** Apache-2.0 requires preserving NOTICE files when redistributing. Mitigation: include upstream NOTICE in the package root.

## Maintenance cadence

- **SHA bump:** when upstream tags a release, or every ~4 weeks if untagged. Edit `manifest.yaml`, `make build`, `make check`, commit, open PR to catalog.
- **New upstream agents:** add to `manifest.yaml`, regenerate, PR. (Anthropic added agents between the news post and the repo; expect more.)
- **Schema changes:** if `agentcompanies/v1` evolves, bump generator and re-emit.

## Out of scope (deferred)

- aqora-specific extensions, integrations, or branding.
- A standalone `aqora-io/claude-for-financial-services-agent-company` repo (Approach C from brainstorming). Revisit if/when we add aqora-specific content.
- Coordinating with Anthropic on official endorsement.
- Translating partner-built plugins (LSEG, S&P Global) — those have separate licensing and aren't in `anthropics/financial-services` proper.

## Working directory decision

The generated package is built directly inside the `paperclipai/companies` fork at `~/code/paperclipai-companies/claude-for-financial-services/`. This puts the new company directory and the catalog-root `README.md` table edit into the same commits, which is what the PR needs to look like anyway. The current scratch dir at `~/code/claude-fsi-agent-company/` exists only to hold this design doc until the fork is set up; the doc moves into the fork at the start of implementation.

## Open questions for implementation

- Whether to open a discussion issue on the catalog before opening the PR (lower-risk path raised in brainstorming, deferred). Default: open the PR directly.
- Org-chart image style — graphviz `dot` is simplest but other catalog entries use varied styles. Default: match the visual style of the closest existing entry that's also referencing upstream skills (`superpowers` or `gstack`).
