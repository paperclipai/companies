---
name: model-routing
description: "Cost-optimize AI agent operations by routing tasks to appropriate models based on complexity. Prevents expensive models from handling simple tasks."
---

# Model Routing

## Principle

Not every task needs the most expensive model. Route work to the cheapest model that can handle it reliably.

## Routing Table

| Task Type | Model Tier | Examples |
|-----------|-----------|---------|
| Simple lookup, formatting, templates | Tier 1 (cheapest) | Email from template, format report, parse JSON |
| Standard analysis, writing, coding | Tier 2 (mid) | Write blog post, debug code, analyze competitor |
| Complex reasoning, architecture, strategy | Tier 3 (expensive) | System design, multi-step planning, strategic analysis |
| Critical decisions, novel problems | Tier 4 (best available) | Security review, financial modeling, customer escalation |

## Rules

1. Default to Tier 2 unless the task clearly requires more or less
2. Never use Tier 4 for templated operations
3. If a Tier 2 task fails, retry once before escalating to Tier 3
4. Batch simple tasks: send 5 template emails in one Tier 1 call, not 5 separate calls
5. Log model usage for monthly cost review

## Cost Awareness

- Track monthly spend per agent
- Set budget alerts at 80% of monthly allocation
- If budget is tight, downgrade non-critical tasks one tier
- Research and monitoring tasks are the first to downgrade
