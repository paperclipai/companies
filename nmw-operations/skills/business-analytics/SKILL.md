---
name: business-analytics
description: "KPI definitions, report formats, and analysis standards for home service business operations. Covers revenue tracking, seasonal forecasting, route profitability, and variance analysis."
---

# Business Analytics for Home Service Operations

## KPI Definitions

### Revenue Metrics
- **Gross Revenue:** Total invoiced amount before any adjustments
- **Net Revenue:** Gross minus refunds, credits, and write-offs
- **Revenue per Route Day:** Total revenue / number of days with scheduled work
- **Revenue per Job:** Total revenue / number of completed jobs
- **Average Job Value:** Mean invoice amount across all job types

### Operational Metrics
- **Jobs Completed:** Count of services delivered in period
- **Completion Rate:** Jobs completed / jobs scheduled (target: 95%+)
- **Route Density:** Average jobs per route day per geographic zone
- **Drive Time Ratio:** Drive time / total work time (lower is better, target: < 25%)
- **Same-Day Invoice Rate:** Invoices sent day-of / jobs completed (target: 100%)

### Customer Metrics
- **New Customers:** First-time service in period
- **Churn Rate:** Customers who cancelled / total active customers
- **Lifetime Value (LTV):** Average revenue per customer over their active lifetime
- **Estimate Conversion Rate:** Estimates approved / estimates sent (target: 40%+)
- **Response Time:** Time from lead submission to first contact (target: < 1 hour)

### Financial Health
- **Operating Margin:** (Revenue - COGS - Operating Expenses) / Revenue
- **Cash Runway:** Current cash / average monthly burn rate
- **Seasonal Reserve:** Cash saved during peak months to cover off-season expenses

## Report Formats

### Weekly Report
```
## Week of {{date_range}}
**Revenue:** ${{amount}} ({{yoy_change}} YoY, {{vs_projection}} vs projection)
**Jobs:** {{count}} completed ({{completion_rate}} completion rate)
**New Customers:** {{new_count}} ({{conversion_rate}} estimate conversion)
**Notable:** {{one_sentence_highlight}}
**Action:** {{one_sentence_recommendation}}
```

### Monthly Report
Same structure as weekly, plus:
- Seasonal trend comparison (same month prior year)
- Cash flow summary (in vs out)
- Customer churn analysis
- Route profitability by zone

## Variance Thresholds

| Metric | Normal Range | Alert Threshold |
|--------|-------------|-----------------|
| Weekly revenue | +/- 5% vs projection | > 15% deviation |
| Completion rate | 93-100% | < 90% |
| Estimate conversion | 35-50% | < 25% |
| Churn (monthly) | 2-5% | > 8% |
| Response time | < 2 hours | > 4 hours |

## Seasonal Adjustments

Home service businesses have predictable seasonal patterns. Always compare same-period-prior-year, not sequential months.

- **Spring ramp (Mar-Apr):** Revenue climbs 30-50% month-over-month. Normal.
- **Peak (May-Aug):** Highest revenue. Benchmark all other periods against this.
- **Fall taper (Sep-Oct):** Revenue drops 20-30%. Plan for it.
- **Off-season (Nov-Feb):** Minimal or zero service revenue. Snow removal if offered.
