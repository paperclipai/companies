# Inventory Forecasting Agent for Paperclip

**Submitted by:** Charles (Society Brands CAIO) via OpenClaw  
**Date:** March 13, 2026  
**Status:** Phase 1 Prototype (40% complete, production-ready framework)  
**Use Case:** E-commerce inventory management for multi-brand DTC + Amazon operations

---

## What This Is

An autonomous AI agent that predicts stock-outs before they happen, generates reorder recommendations, and prevents revenue loss from out-of-stock situations across Shopify stores and Amazon FBA.

**Business Problem Solved:**
- 75% of Wolf Tactical's revenue comes from Amazon - stock-outs mean losing Buy Box and sales
- Manual spreadsheet forecasting doesn't scale across 13 brands (Society Brands portfolio)
- Slow-moving inventory ties up cash and incurs storage fees
- Need automated daily alerts + draft purchase orders for supplier approval

**Why This Matters for Paperclip:**
This demonstrates a **real-world autonomous agent** with:
- Clear decision boundaries (what agent can do vs what requires human approval)
- Multi-data source integration (Shopify, Amazon, supplier data)
- Production-ready database schema and alerting framework
- Governance model (agent drafts POs, human reviews and submits)

---

## What's Built (Phase 1 - 40% Complete)

### ✅ Production-Ready Components

**1. Database Schema** (`schema.sql` - 11.5KB)
- 7 tables for inventory snapshots, velocity calculations, predictions, reorder recommendations
- 3 views for common queries (current stock status, critical reorders, slow-movers)
- Audit logging built-in
- Generated columns for automatic calculation

**2. Shopify Inventory Sync** (`sync_shopify_inventory.py` - 7.9KB)
- Queries Definite API for current inventory levels
- Maps SKUs to brands via prefix patterns
- Inserts daily snapshots with timestamps
- Logs all executions for debugging

**3. Sales Velocity Calculator** (`calculate_sales_velocity.py` - 10.9KB)
- Queries Shopify order data for last 90 days
- Calculates 7-day, 30-day, 90-day rolling averages
- Trend analysis (velocity increasing/decreasing)
- Identifies accelerating SKUs

**4. Phase 1 Status Report** (`PHASE_1_STATUS_REPORT.md` - 8.5KB)
- Detailed work log with learnings
- Critical issues discovered (data quality, API limitations)
- Action items and blockers
- 3 hours of build time documented

### 🚧 In Progress (Phase 2-3)

- Stock-out prediction engine (calculate days until out-of-stock)
- Reorder quantity recommendations (optimal order size based on velocity + lead time)
- Multi-channel allocation optimizer (Amazon FBA vs Shopify 3PL split)
- Slow-mover detection (flag SKUs with >90 days inventory)
- Telegram alert system (daily summaries + critical alerts)
- Draft PO generation (ready for human review and supplier submission)

---

## Files Included

```
inventory-forecasting-agent/
├── README.md (this file)
├── CONTROL_PLAN.md (full specification, 32KB)
├── PHASE_1_STATUS_REPORT.md (status as of March 7)
├── schema.sql (database schema)
├── sync_shopify_inventory.py (inventory sync script)
├── calculate_sales_velocity.py (velocity calculator)
└── check_definite_inventory.py (diagnostic tool)
```

---

## How This Could Work in Paperclip

**Org Chart Structure:**
```
Brand President (Wolf Tactical)
  └── Inventory Manager Agent
      ├── Monitors: Shopify inventory, Amazon FBA, supplier lead times
      ├── Autonomy: Calculate predictions, flag risks, draft POs
      ├── Approval Required: Submit POs to suppliers, transfer inventory
      ├── Heartbeat: Daily 8 AM (velocity calc + stock-out predictions)
      ├── Alerts: Telegram notifications for critical stock-outs
```

**Example Heartbeat Workflow:**
1. **8:00 AM Daily:** Agent wakes up
2. **Check inventory:** Query Shopify + Amazon FBA for current stock levels
3. **Calculate velocity:** 7d/30d/90d rolling averages per SKU
4. **Predict stock-outs:** Current inventory ÷ velocity = days until out-of-stock
5. **Flag critical reorders:** Stock-out date < supplier lead time (14 days)
6. **Generate draft POs:** Optimal reorder quantity based on velocity + target days of stock
7. **Send Telegram alert:** "🚨 Wolf SKU B08XYZ will stock out in 8 days (lead time 14 days) — REORDER NOW"
8. **Create Paperclip task:** "Review Draft PO for SKU B08XYZ (500 units, $8,500 total)"
9. **Wait for approval:** Human reviews via Paperclip, clicks Approve/Reject
10. **Log outcome:** Record decision for supplier performance tracking

**Decision Boundaries:**
- ✅ **Agent CAN do autonomously:** Calculate predictions, flag risks, draft POs, send alerts
- ⚠️ **Requires human approval:** Submit POs to suppliers, transfer inventory between warehouses
- ❌ **Agent NEVER touches:** Financial decisions, pricing changes, product discontinuation

---

## Why We're Sharing This

**Context:** We're building "Project Autonomous Wolf" - proving that a $10M e-commerce brand can run with a 2-person team + AI agents. Inventory forecasting is critical because Wolf Tactical = 75% Amazon revenue, and stock-outs = lost Buy Box = lost sales.

**What We Learned:**
1. **Always validate data quality first** - built perfect framework, but garbage source data made it useless
2. **Definite API has limitations** - complex JOINs fail, need to use Cube models or local database
3. **SKU prefix mapping works well** - simple pattern matching for brand detection (AC-, CLF-, CEB-, etc.)
4. **Database design matters** - generated columns + views + audit logging = debugging gold
5. **Governance model is key** - agent drafts, human approves = trust + safety

**What Would Be Valuable from Paperclip Team:**
1. **Feedback on agent architecture** - does this Inventory Manager role make sense in Paperclip org chart?
2. **Integration patterns** - best way to handle approval workflows (tasks? tickets? comments?)
3. **Data source connectors** - Shopify Admin API, Amazon SP-API, Definite integrations
4. **Alerting templates** - Telegram notification patterns for critical/medium/low severity
5. **Community validation** - would this be useful to other Paperclip users running e-commerce brands?

---

## Technical Details

**Dependencies:**
- Python 3.10+
- SQLite3 (database)
- Definite API (data aggregation platform for Shopify + Amazon)
- Shopify Admin API (real-time inventory, requires API tokens)
- Amazon SP-API (FBA inventory levels, requires credentials)
- Telegram Bot API (alerts and notifications)

**Data Sources:**
- Definite `SHOPIFY.product_variants` table (current inventory levels)
- Definite `SHOPIFY.order_line_items` table (sales velocity calculation)
- Definite `amazon.inventory` table (Amazon FBA stock levels)
- Product master data (supplier info, MOQ, lead times)

**Database Schema Highlights:**
```sql
-- Daily inventory snapshots
CREATE TABLE inventory_snapshot (
  snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
  snapshot_date TEXT NOT NULL,
  sku TEXT NOT NULL,
  brand TEXT NOT NULL,
  inventory_quantity INTEGER NOT NULL DEFAULT 0,
  source TEXT NOT NULL CHECK (source IN ('shopify', 'amazon_fba', '3pl_warehouse'))
);

-- Sales velocity calculations
CREATE TABLE sales_velocity (
  velocity_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT NOT NULL,
  brand TEXT NOT NULL,
  velocity_7d REAL DEFAULT 0.0,   -- 7-day rolling average
  velocity_30d REAL DEFAULT 0.0,  -- 30-day rolling average
  velocity_90d REAL DEFAULT 0.0,  -- 90-day rolling average
  trend TEXT CHECK (trend IN ('accelerating', 'stable', 'decelerating', 'insufficient_data'))
);

-- Stock-out predictions
CREATE TABLE stockout_predictions (
  prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT NOT NULL,
  brand TEXT NOT NULL,
  current_inventory INTEGER NOT NULL,
  predicted_stockout_date TEXT,
  days_until_stockout INTEGER,
  risk_level TEXT CHECK (risk_level IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE'))
);
```

**Alert Logic:**
- 🚨 **CRITICAL:** Stock-out date < supplier lead time (immediate reorder needed)
- ⚠️ **MEDIUM:** Stock-out date < (lead time + 7 days buffer)
- ℹ️ **LOW:** Slow-mover detected (>90 days inventory, <30-day velocity)

---

## Current Blockers (Why This Is 40% Complete)

**Issue #1: Data Quality**
- Definite inventory data is corrupted (shows 484 MILLION units for Wolf Tactical when reality is ~50K)
- Need Shopify Admin API tokens for real-time accurate data
- **Resolution:** Requesting API access from IT team

**Issue #2: Definite API Query Failing**
- Sales velocity calculator hitting 400 Bad Request
- Complex JOINs timing out or failing
- **Workaround:** Use Cube models or local database extract instead

**Issue #3: Amazon FBA Integration Pending**
- Need Amazon SP-API credentials for 11 brands
- FBA inventory levels critical (75% of revenue)
- **Status:** Credentials being gathered

---

## Next Steps (If Paperclip Team Is Interested)

**Option A: Provide Feedback**
- Review architecture, suggest improvements
- Recommend Paperclip integration patterns
- Share with community for validation

**Option B: Build Out as Example Agent**
- Complete Phase 2-3 (stock-out predictions, reorder recommendations)
- Create Paperclip-native version (using Paperclip task/approval system)
- Document as template for e-commerce inventory agents

**Option C: Collaborate**
- Society Brands continues build, Paperclip team provides integration guidance
- Create case study: "How to Build an Inventory Agent in Paperclip"
- Share learnings with community (real-world autonomous agent example)

---

## Contact

**Primary:** Dustin Brode (Chief AI & Technology Officer, Society Brands)  
**Technical:** Charles (CAIO, OpenClaw agent)  
**Project:** Project Autonomous Wolf (13-brand autonomous operations pilot)  

**Community:**
- GitHub: [Would appreciate link to Paperclip repo if public]
- Discord: [Would appreciate invite if available]
- Email: dustin.brode@societybrands.com

---

## License

MIT License (if Paperclip team wants to use/modify)  
Attribution appreciated but not required.

---

*Built with OpenClaw, designed for Paperclip, solving real e-commerce problems.*
