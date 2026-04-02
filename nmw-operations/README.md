# NMW Operations

AI-powered operations company for home service businesses. 7 specialized agents handle everything from lead intake to invoicing, SEO to analytics.

Built by [No Mow Worries](https://nomowworriesco.com), a lawn care company in Aurora, CO that uses this agent swarm to run day-to-day operations. This is the first home service operations company in the companies.sh directory.

## Agents

| Agent | Role | What They Do |
|-------|------|-------------|
| **Henry** | CTO | Orchestrates all work. Routes tasks to specialists. Never writes code or copy. |
| **Forge** | Lead Engineer | Builds websites, APIs, dashboards, widgets, CLI tools. Mobile-first, test-driven. |
| **Clawd** | CRM Ops | Estimates, scheduling, invoicing, follow-ups, data hygiene. Quote requests are #1 priority. |
| **Ink** | Communications | Every customer-facing word: emails, SMS, follow-ups, complaints. Warm, direct, human. |
| **Maven** | Marketing | SEO, content, ads, lead gen. Local-first strategy targeting real search queries. |
| **Scout** | Intelligence | Competitor monitoring, market research, tech evaluation. Signal over volume. |
| **Numbers** | Analytics | Revenue tracking, KPIs, seasonal forecasting, variance analysis. Data into decisions. |

## Skills

| Skill | Used By | Description |
|-------|---------|-------------|
| `local-seo` | Maven | SEO audits, schema markup, meta tags, GSC diagnostics |
| `customer-comms` | Ink | Brand voice, email/SMS templates, escalation rules |
| `business-analytics` | Numbers | KPI definitions, report formats, variance thresholds |
| `service-pricing` | Clawd | Per-sqft pricing, lot measurement, estimate generation |
| `self-improvement` | All agents | Learning capture, error logging, continuous improvement |
| `model-routing` | Henry | Cost-optimized model selection for task complexity |
| `task-dispatch` | Henry | Task lifecycle, proof requirements, escalation rules |

## Org Chart

```
            Owner (CEO)
                |
           Henry (CTO)
          /   |   |   \   \    \
      Forge Clawd Ink Maven Scout Numbers
```

## Key Principles

1. **Proof required.** No agent reports "done" without evidence.
2. **Customer ID is king.** Never search CRM by name or email.
3. **Templates over custom.** Consistency beats creativity for ops comms.
4. **Every tool is a product.** Architecture is modular and multi-tenant-ready.
5. **Signal over volume.** Research returns findings that change decisions.
6. **Self-improving.** Every agent logs learnings and reviews them weekly.

## Import

```bash
paperclipai company import --from ./nmw-operations
```

## Customization

This template is designed for home service businesses but can be adapted:

- **Service type:** Update `service-pricing` with your rates and services
- **Location:** Update SEO skills with your city and service area
- **Brand voice:** Update `customer-comms` with your tone and templates
- **CRM:** Clawd's instructions are CRM-agnostic. Point at your CRM's API.
- **Agents:** Add or remove specialists based on your operation's size

## License

MIT
