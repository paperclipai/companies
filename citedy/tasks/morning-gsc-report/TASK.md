---
schema: agentcompanies/v1
kind: task
slug: morning-gsc-report
name: Morning GSC Report & Content Action
description: Daily routine — check GSC performance, identify opportunities, write and publish a mini-article with social posts.
assignee: ../agents/gsc-analyst/AGENTS.md
tags:
  - daily
  - gsc
  - automated
---

# Morning GSC Report & Content Action

A daily task that turns search data into published content.

## Steps

1. **Pull GSC Report**
   ```
   GET /api/agent/gsc/report
   ```
   Review: clicks, impressions, position changes, top queries

2. **Identify Opportunity**
   Pick the top keyword from `articleSuggestions` — high impressions, not yet covered

3. **Generate Article**
   ```
   POST /api/agent/autopilot
   { "topic": "<suggested keyword>", "size": "mini" }
   ```

4. **Create Social Adaptations**
   ```
   POST /api/agent/adapt
   { "article_id": "<id>", "platforms": ["linkedin", "x_thread", "facebook"] }
   ```

5. **Publish Everywhere**
   ```
   POST /api/agent/publish
   { "adaptationId": "<id>", "action": "now" }
   ```

## Expected Outcome

- 1 SEO article published on blog
- 3+ social media posts live
- Content gap closed for a high-potential keyword
- Total cost: ~15-30 credits (~$0.15-0.30)
