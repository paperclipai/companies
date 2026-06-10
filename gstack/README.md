# GStack

> Engineering company powered by gstack workflow skills — distinct cognitive modes for product vision, design critique, technical planning, security auditing, code review, shipping, deployment, and QA

> An [Agent Company](https://agentcompanies.io) based on [gstack](https://github.com/garrytan/gstack) — engineering workflow skills for headless browsing, QA testing, PR review, shipping, retrospectives, and plan reviews

![Org Chart](images/org-chart.png)

## What's Inside

> This is an [Agent Company](https://agentcompanies.io) package from [Paperclip](https://paperclip.ing)

| Content | Count |
|---------|-------|
| Agents | 5 |
| Skills | 58 |
| Upstream gstack | 1.57.9.0 |

### Agents

| Agent | Role | Reports To |
|-------|------|------------|
| CEO | CEO | — |
| CTO | CTO | ceo |
| QA Engineer | Engineer | cto |
| Release Engineer | Engineer | cto |
| Staff Engineer | Engineer | cto |

### Skills

| Skill | Description | Source |
|-------|-------------|--------|
| autoplan | Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisions using 6 decision principles. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/autoplan/SKILL.md) |
| benchmark | Performance regression detection using the browse daemon. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/benchmark/SKILL.md) |
| benchmark-models | Cross-model benchmark for gstack skills. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/benchmark-models/SKILL.md) |
| browse | Fast headless browser for QA testing and site dogfooding. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/browse/SKILL.md) |
| canary | Post-deploy canary monitoring. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/canary/SKILL.md) |
| careful | Safety guardrails for destructive commands. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/careful/SKILL.md) |
| codex | OpenAI Codex CLI wrapper — three modes. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/codex/SKILL.md) |
| context-restore | Restore working context saved earlier by /context-save. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/context-restore/SKILL.md) |
| context-save | Save working context. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/context-save/SKILL.md) |
| cso | Chief Security Officer mode. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/cso/SKILL.md) |
| design-consultation | Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color, layout, spacing, motion), and generates font+color preview... (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/design-consultation/SKILL.md) |
| design-html | Design finalization: generates production-quality Pretext-native HTML/CSS. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/design-html/SKILL.md) |
| design-review | Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/design-review/SKILL.md) |
| design-shotgun | Design shotgun: generate multiple AI design variants, open a comparison board, collect structured feedback, and iterate. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/design-shotgun/SKILL.md) |
| devex-review | Live developer experience audit. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/devex-review/SKILL.md) |
| document-generate | Generate missing documentation from scratch for a feature, module, or entire project. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/document-generate/SKILL.md) |
| document-release | Post-ship documentation update. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/document-release/SKILL.md) |
| freeze | Restrict file edits to a specific directory for the session. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/freeze/SKILL.md) |
| gstack | Fast headless browser for QA testing and site dogfooding. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/SKILL.md) |
| gstack-openclaw-ceo-review | Use when asked to review a plan, challenge a proposal, run a CEO review, poke holes in an approach, think bigger about scope, or decide whether to expand or reduce the plan. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/openclaw/skills/gstack-openclaw-ceo-review/SKILL.md) |
| gstack-openclaw-investigate | Use when asked to debug, fix a bug, investigate an error, or do root cause analysis, and when users report errors, stack traces, unexpected behavior, or say something stopped working. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/openclaw/skills/gstack-openclaw-investigate/SKILL.md) |
| gstack-openclaw-office-hours | Use when asked to brainstorm, evaluate whether an idea is worth building, run office hours, or think through a new product idea or design direction before any code is written. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/openclaw/skills/gstack-openclaw-office-hours/SKILL.md) |
| gstack-openclaw-retro | Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. Team-aware with per-person contributions, praise, and growth areas. Use when asked for weekly retro, what shipped this week, or engineering retrospective. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/openclaw/skills/gstack-openclaw-retro/SKILL.md) |
| gstack-upgrade | Upgrade gstack to the latest version. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/gstack-upgrade/SKILL.md) |
| guard | Full safety mode: destructive command warnings + directory-scoped edits. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/guard/SKILL.md) |
| hackernews-frontpage | Scrape the Hacker News front page (titles, points, comment counts). | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/browser-skills/hackernews-frontpage/SKILL.md) |
| health | Code quality dashboard. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/health/SKILL.md) |
| investigate | Systematic debugging with root cause investigation. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/investigate/SKILL.md) |
| ios-clean | Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/ios-clean/SKILL.md) |
| ios-design-review | Visual design audit for iOS apps on real hardware. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/ios-design-review/SKILL.md) |
| ios-fix | Autonomous iOS bug fixer. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/ios-fix/SKILL.md) |
| ios-qa | Live-device iOS QA for SwiftUI apps. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/ios-qa/SKILL.md) |
| ios-sync | Regenerate the iOS debug bridge against the latest upstream gstack templates. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/ios-sync/SKILL.md) |
| land-and-deploy | Land and deploy workflow. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/land-and-deploy/SKILL.md) |
| landing-report | Read-only queue dashboard for workspace-aware ship. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/landing-report/SKILL.md) |
| learn | Manage project learnings. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/learn/SKILL.md) |
| make-pdf | Turn any markdown file into a publication-quality PDF. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/make-pdf/SKILL.md) |
| office-hours | YC Office Hours — two modes. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/office-hours/SKILL.md) |
| open-gstack-browser | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/open-gstack-browser/SKILL.md) |
| pair-agent | Pair a remote AI agent with your browser. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/pair-agent/SKILL.md) |
| plan-ceo-review | CEO/founder-mode plan review. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/plan-ceo-review/SKILL.md) |
| plan-design-review | Designer's eye plan review — interactive, like CEO and Eng review. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/plan-design-review/SKILL.md) |
| plan-devex-review | Interactive developer experience plan review. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/plan-devex-review/SKILL.md) |
| plan-eng-review | Eng manager-mode plan review. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/plan-eng-review/SKILL.md) |
| plan-tune | Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/plan-tune/SKILL.md) |
| qa | Systematically QA test a web application and fix bugs found. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/qa/SKILL.md) |
| qa-only | Report-only QA testing. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/qa-only/SKILL.md) |
| retro | Weekly engineering retrospective. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/retro/SKILL.md) |
| review | Pre-landing PR review. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/review/SKILL.md) |
| scrape | Pull data from a web page. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/scrape/SKILL.md) |
| setup-browser-cookies | Import cookies from your real Chromium browser into the headless browse session. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/setup-browser-cookies/SKILL.md) |
| setup-deploy | Configure deployment settings for /land-and-deploy. | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/setup-deploy/SKILL.md) |
| setup-gbrain | Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain, register MCP, capture per-remote trust policy. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/setup-gbrain/SKILL.md) |
| ship | Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/ship/SKILL.md) |
| skillify | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/skillify/SKILL.md) |
| spec | Turn vague intent into a precise, executable spec in five phases. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/spec/SKILL.md) |
| sync-gbrain | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. Wraps the gstack-gbrain-sync orchestrator with state (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/sync-gbrain/SKILL.md) |
| unfreeze | Clear the freeze boundary set by /freeze, allowing edits to all directories again. (gstack) | [github](https://github.com/garrytan/gstack/blob/8241949357263be64013a8410171def68cff920c/unfreeze/SKILL.md) |

## Getting Started

```bash
npx companies.sh add paperclipai/companies/gstack
```

See [Paperclip](https://paperclip.ing) for more information.

---
Exported from [Paperclip](https://paperclip.ing) on 2026-06-10
Updated from [gstack](https://github.com/garrytan/gstack/tree/8241949357263be64013a8410171def68cff920c) 1.57.9.0.
