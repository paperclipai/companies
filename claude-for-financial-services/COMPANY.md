---
schema: agentcompanies/v1
slug: claude-for-financial-services
name: Claude for Financial Services
description: 10-agent finance company — coverage, research, fund admin, and onboarding
  — ported from anthropics/financial-services into the Agent Companies format.
version: 0.1.0
license: Apache-2.0
authors:
- name: Jannes Stubbemann
  email: jannes@paperclip.inc
goals:
- Draft analyst work product (models, memos, reconciliations) for human review.
- Cover the four FSI workflow areas Anthropic shipped — coverage & advisory, research
  & modeling, fund admin & finance ops, operations & onboarding.
- Stage every output for human sign-off — no agent here executes trades, posts to
  a ledger, or approves onboarding.
tags:
- finance
- fsi
- investment-banking
- equity-research
- private-equity
- fund-admin
- kyc
metadata:
  upstream:
    repo: anthropics/financial-services
    commit: 57772c3f1607229fba0270f94abf3c976bbd852f
    license: Apache-2.0
  affiliation: Community port. Not affiliated with or endorsed by Anthropic.
---
# Claude for Financial Services

10-agent finance company — coverage, research, fund admin, and onboarding — ported from anthropics/financial-services into the Agent Companies format.

## Boundaries

Nothing in this package constitutes investment, legal, tax, or accounting advice.
These agents draft analyst work product (models, memos, research notes,
reconciliations) for review by a qualified professional. They do not make
investment recommendations, execute transactions, bind risk, post to a ledger,
or approve onboarding; every output is staged for human sign-off.

## Teams

- **Coverage & Advisory** (`teams/coverage-advisory/TEAM.md`) — Client-facing pitch and meeting workflows.
- **Research & Modeling** (`teams/research-modeling/TEAM.md`) — Sector research, earnings, and live financial modeling in Excel.
- **Fund Admin & Finance Ops** (`teams/fund-admin-finance-ops/TEAM.md`) — Valuation, close, and statement workflows for fund administrators.
- **Operations & Onboarding** (`teams/operations-onboarding/TEAM.md`) — KYC and client onboarding workflows.

