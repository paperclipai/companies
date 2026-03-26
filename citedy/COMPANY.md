---
schema: agentcompanies/v1
kind: company
slug: citedy
name: Citedy
description: AI-powered SEO content marketing company. Scouts trends, analyzes competitors, generates articles in 55 languages with AI illustrations and voice-over, publishes across 9 social platforms, creates lead magnets and viral video shorts. Fully autonomous content pipeline from research to publication.
version: "3.4.0"
license: Proprietary
authors:
  - name: Citedy
    url: https://www.citedy.com
tags:
  - seo
  - content-marketing
  - ai-agents
  - social-media
  - lead-generation
  - video
  - gsc
  - trend-scouting
  - competitor-analysis
metadata:
  website: https://www.citedy.com
  api_base: https://www.citedy.com/api/agent
  mcp_endpoint: https://mcp.citedy.com/mcp
  pricing: credit-based (1 credit = $0.01 USD)
  registration: https://www.citedy.com/api/agent/register
---

# Citedy — AI Content Marketing Company

Citedy is a fully autonomous AI content marketing team. Connect it to your AI agent and get a complete marketing department: trend research, competitor intelligence, SEO-optimized content creation, multi-platform social distribution, lead magnet generation, and performance analytics.

## What Citedy Does

1. **Research** — Scout X/Twitter and Reddit for trending topics, discover and deep-analyze competitors, find content gaps
2. **Create** — Generate SEO- and GEO-optimized articles (mini to pillar) in 55 languages with AI illustrations and voice-over
3. **Distribute** — Adapt and publish to X, LinkedIn, Facebook, Reddit, Instagram, Threads, YouTube Shorts, and Shopify
4. **Convert** — Generate lead magnets (checklists, swipe files, frameworks) for lead capture
5. **Analyze** — Google Search Console performance reports with content opportunity suggestions
6. **Automate** — Cron-based content sessions, scheduled publishing, webhook notifications

## Teams

- [Content Marketing Team](teams/content-marketing/TEAM.md) — the core operational team

## Getting Started

1. Register an agent: `POST https://www.citedy.com/api/agent/register`
2. Approve at the returned URL
3. Poll `GET /api/agent/pending/{id}` until approved
4. Use the API key for all subsequent calls

All endpoints are authenticated via `Authorization: Bearer citedy_agent_*` header.
