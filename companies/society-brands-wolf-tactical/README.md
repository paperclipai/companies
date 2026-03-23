# Society Brands — Wolf Tactical Agent Submissions

**Company:** Society Brands (13-brand DTC e-commerce portfolio, ~$120M annual revenue)
**Project:** Project Autonomous Wolf — proving $10M Wolf Tactical brand can run with 2 humans + AI agents
**Contact:** Dustin Brode (dustin.brode@societybrands.com)

---

## Submitted Agents

### 1. [Inventory Forecasting Agent](./inventory-forecasting-agent/)

**Status:** Phase 1 prototype (40% complete, production-ready framework)
**Use Case:** Predicts stock-outs before they happen, generates reorder recommendations for DTC + Amazon

**What's Included:**
- Production database schema (7 tables + 3 views) for multi-brand inventory tracking
- Shopify Admin API sync script with velocity calculation
- Sales velocity calculator with seasonality adjustments
- Full 37-page control plan and Phase 1 status report

**Why It Matters:** Wolf Tactical is 75% Amazon — a stock-out means losing the Buy Box, which cascades to lost sales, ranking drops, and review suppression risk. Manual reorder tracking can't keep up with 172 SKUs across Amazon + Shopify.

**Decision Boundaries:** Agent forecasts and recommends; all actual reorder commitments escalate to human approval before execution.

---

### 2. [Landing Page Router (Auto A/B Testing)](./landing-page-router/)

**Status:** 90% complete, production-deployed at [webapprouter.netlify.app](https://webapprouter.netlify.app)
**Use Case:** Automated A/B testing with auto-kill logic for underperforming landing page variants

**What's Included:**
- Netlify serverless router with weighted traffic splitting and segment targeting
- GA4 Data API integration for conversion tracking
- n8n auto-kill workflow (kills variants with <1.5% CVR after 200 sessions)
- Process documentation + full SOP

**Why It Matters:** Manual A/B testing review cycles take 1-2 weeks. This system kills losers automatically within 6 hours of hitting statistical significance, reallocates traffic to winners without human intervention.

**What Remains:** Connect traffic from ad platforms, activate first Wolf Tactical test campaign.

---

## Architecture Notes

Both agents follow these patterns relevant to Paperclip integration:

1. **Clear decision boundaries** — agents monitor and recommend; humans (or Paperclip approval flows) approve actions with financial impact
2. **Multi-data source integration** — Shopify, Amazon, GA4, n8n, Netlify
3. **Escalation-first design** — any spend, reorder, or policy decision routes to the Brand President approval queue before execution
4. **Heartbeat-compatible** — designed to run on hourly/6-hour cadences without persistent state

---

## Context: Project Autonomous Wolf

Society Brands is running a 54-day sprint (Feb 6 – Mar 31, 2026) to prove fully autonomous operations for Wolf Tactical. The full Paperclip agent team:

- **Brand President** (claude-sonnet, this agent) — strategic/operational lead
- **Charles — EVP Technology & Data** (OpenClaw) — technical execution, data access
- **Wolf Amazon Agent** — storefront health, Buy Box, suppression monitoring
- **Wolf Finance Agent** — bookkeeping, P&L, settlement reconciliation
- **Wolf Inventory Agent** — stock health, reorder planning
- **Wolf Creative Agent** — creative pipeline, asset production
- **Wolf Ads Agent** — paid media monitoring, campaign QA
- **Wolf Email Agent** — campaign calendar, deliverability
- **Wolf Customer Support Agent** — queue health, SLA monitoring

These two submitted agents are the automation layer that the Paperclip agent team depends on for data-driven decisions.
