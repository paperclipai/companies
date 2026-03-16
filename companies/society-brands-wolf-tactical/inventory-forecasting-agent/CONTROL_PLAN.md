# Inventory Forecasting Agent - Plan Control Document

**Project Owner:** Dustin Brode  
**Project Lead:** Charles (CATO)  
**Document Version:** 1.0  
**Date:** March 6, 2026  
**Status:** Approved for Build  
**Timeline:** 1-2 weeks (Phase 3, Days 29-33)

---

## 1. Executive Summary

**Project Goal:** Build an AI agent that predicts stock-outs before they happen, recommends optimal reorder quantities, and prevents revenue loss from Amazon Buy Box loss and Shopify out-of-stock situations.

**Business Impact:**
- **Prevent stock-out revenue loss:** Wolf Tactical = 75% Amazon revenue. Stock-outs = lose Buy Box = lose sales.
- **Optimize cash flow:** Right-size inventory (avoid overstocking cash trap + Amazon FBA long-term storage fees).
- **Eliminate manual forecasting:** Replace spreadsheets with automated daily alerts + reorder recommendations.
- **Enable 13-brand scale:** Automated forecasting is the ONLY way to manage inventory across Society Brands portfolio.
- **Detect dying inventory:** Flag slow-movers for clearance before they become dead cash.

**Timeline:** 1-2 weeks (Target: March 17, 2026)

**Alternative:** Teikametrics offers inventory forecasting module. Could buy instead of build. Decision: Dustin to evaluate cost vs build effort.

---

## 2. Project Objectives

### Primary Objectives

**Predictive Stock-Out Alerts**
- Daily scan of all SKUs across Shopify + Amazon
- Calculate days until stock-out based on current velocity
- Alert when stock-out date < (supplier lead time + safety buffer)
- Flag SKUs requiring immediate reorder

**Reorder Quantity Recommendations**
- Calculate optimal reorder quantity based on:
  - Current velocity (7-day, 30-day, 90-day rolling averages)
  - Supplier lead time
  - Target days of stock (configurable per SKU)
  - Seasonality factors
  - Promotional calendar
- Generate draft PO for supplier approval (NOT auto-submit)

**Multi-Channel Allocation Optimization**
- Recommend split between Amazon FBA vs Shopify 3PL based on:
  - Historical channel mix (75% Amazon, 25% Shopify for Wolf)
  - Fulfillment costs (FBA fees vs 3PL)
  - Customer location patterns
- Optimize for lowest total fulfillment cost while maintaining service levels

**Slow-Mover Detection**
- Flag SKUs with <30-day velocity and >90 days current inventory
- Recommend clearance pricing, bundling, or discontinuation
- Prevent dead inventory cash trap

### Success Criteria

✅ Agent operational for Wolf Tactical within 1 week  
✅ Daily stock-out alerts delivered to Telegram with correct predictions  
✅ Zero false negatives on critical stock-outs (tested against historical data)  
✅ Reorder recommendations accurate within 10% of actual optimal quantity  
✅ Multi-channel allocation recommendations save 5%+ on fulfillment costs  
✅ Slow-mover detection flags 100% of SKUs with >120 days inventory  
✅ Draft POs ready for supplier approval (includes SKU, quantity, lead time, cost)  
✅ System scales to 13 brands without performance degradation  

---

## 3. Scope Definition

### ✅ IN SCOPE

**Monitoring Coverage:**

**Stock-Out Prediction:**
- Daily velocity calculation (7-day, 30-day, 90-day rolling averages)
- Trend detection (velocity increasing/decreasing)
- Stock-out date prediction (current inventory ÷ velocity)
- Reorder point triggers (lead time + safety buffer)
- Promotional impact modeling (upcoming sales events)

**Inventory Health:**
- Current inventory levels (Shopify + Amazon FBA + 3PL warehouses)
- Stranded inventory integration (from Milan's Amazon Agent)
- In-transit inventory (POs placed but not received)
- Reserved inventory (unfulfilled orders)
- Available-to-sell calculation (total - reserved - safety stock)

**Multi-Channel Optimization:**
- Historical channel mix analysis (Amazon vs Shopify sales by SKU)
- Fulfillment cost comparison (FBA fees vs 3PL per unit)
- Geographic demand patterns (ship-to locations)
- Recommended allocation splits (how much to send to FBA vs 3PL)

**Slow-Mover Detection:**
- Days of inventory calculation (current inventory ÷ 7-day velocity)
- Inventory aging (days since last sale)
- Carrying cost calculation (storage fees + opportunity cost)
- Clearance recommendations (pricing, bundling, discontinuation)

**Purchase Order Automation:**
- Draft PO generation (SKU, quantity, supplier, lead time, cost)
- PO approval workflow (Telegram buttons: Approve / Reject / Modify)
- Supplier lead time tracking (actual vs expected delivery)
- PO history logging (for supplier performance analysis)

### ❌ OUT OF SCOPE (V1)

The following are explicitly excluded from this agent:

- ❌ **Automatic PO submission** (agent drafts POs, human reviews and submits to supplier)
- ❌ **Demand forecasting beyond velocity** (no ML models for seasonality prediction V1)
- ❌ **Supplier relationship management** (quality issues, price negotiations)
- ❌ **Inventory transfers between warehouses** (agent recommends, human executes)
- ❌ **Product bundling decisions** (agent flags slow-movers, human decides bundle strategy)
- ❌ **Pricing strategy** (agent recommends clearance, human sets prices)
- ❌ **New product launch forecasting** (no sales history = no velocity data)

---

## 4. Functional Requirements

### 4.1 Monitoring Cadence

| Metric | Check Frequency | Rationale |
|--------|----------------|-----------|
| Inventory levels | Every 6 hours | Shopify/Amazon update delays |
| Velocity calculation | Daily (8 AM EST) | Sales data stable overnight |
| Stock-out predictions | Daily (8 AM EST) | Proactive reorder alerts |
| Slow-mover detection | Weekly (Sunday 8 PM) | Slower-moving metric |
| Promotional impact | Daily before promo starts | Adjust safety stock |
| PO delivery tracking | Daily (9 AM EST) | Supplier performance |

### 4.2 Alert Strategy

**Severity Levels:**

**🚨 CRITICAL (Immediate Telegram Alert)**
- Stock-out date < supplier lead time (URGENT REORDER NEEDED)
- High-value SKU (>$1K/day revenue) will stock out within 7 days
- Amazon Buy Box lost due to out-of-stock (from Amazon Agent integration)
- Example: "🚨 Wolf SKU B08XYZ will stock out in 8 days (lead time = 14 days) — REORDER NOW or lose $2,100/day revenue"

**⚠️ MEDIUM (Daily Digest Alert)**
- Stock-out date < (lead time + 7 days buffer) but not yet critical
- Slow-mover detected (>90 days inventory, <30-day velocity)
- Multi-channel allocation recommendation (significant cost savings available)
- Example: "⚠️ Wolf SKU B07ABC has 120 days inventory but 25-day velocity — Consider clearance"

**ℹ️ LOW (Weekly Digest Only)**
- Inventory healthy (no action needed)
- PO delivered on time (supplier performance tracking)
- Velocity trends (informational, no action required)

**📊 DAILY SUMMARY (8 AM EST)**
```
📦 Wolf Tactical Inventory Summary (March 6, 2026)

🚨 URGENT REORDERS (3):
• SKU B08XYZ: 8 days until stock-out (lead time 14 days) — $2,100/day revenue at risk
• SKU B07DEF: 10 days until stock-out (lead time 21 days) — $1,400/day revenue at risk  
• SKU B06GHI: 12 days until stock-out (lead time 14 days) — $900/day revenue at risk

⚠️ UPCOMING REORDERS (5):
• SKU B09JKL: 18 days until stock-out (lead time 14 days)
• [4 more...]

📦 SLOW-MOVERS (2):
• SKU B05MNO: 145 days inventory, $4,200 tied up — Recommend clearance
• SKU B04PQR: 98 days inventory, $2,800 tied up — Monitor

✅ HEALTHY INVENTORY (47 SKUs)

📋 DRAFT POS READY FOR APPROVAL (3):
• [View Draft PO #1] — Wolf SKU B08XYZ (500 units, $8,500 total)
```

### 4.3 Decision Boundaries

**What the agent CAN do autonomously:**
- ✅ Calculate velocity and stock-out predictions
- ✅ Generate daily alerts (Telegram)
- ✅ Flag slow-movers for review
- ✅ Recommend multi-channel allocation splits
- ✅ Generate draft POs with recommended quantities
- ✅ Log all calculations and recommendations

**What REQUIRES human approval (NEVER auto-execute):**
- ⚠️ Submit purchase orders to suppliers (agent drafts, human reviews and submits)
- ⚠️ Transfer inventory between warehouses (agent recommends, human executes via Shopify/Amazon)
- ⚠️ Change SKU clearance pricing (agent recommends, human sets prices)
- ⚠️ Discontinue slow-moving products (agent flags, human makes product decisions)
- ⚠️ Adjust safety stock levels (agent uses configured values, human changes config)

**What the agent NEVER touches:**
- ❌ Financial decisions beyond inventory (pricing, supplier payments, contracts)
- ❌ Product development decisions (discontinue vs innovate)
- ❌ Supplier negotiations (pricing, terms, contracts)

---

## 5. Technical Architecture

### 5.1 Platform: Python + Claude API + DuckDB + Telegram

**Primary Components:**
1. **Data Ingestion:** Pull Shopify + Amazon + 3PL inventory data daily
2. **Velocity Engine:** Calculate rolling averages, detect trends
3. **Prediction Engine:** Stock-out date calculation, reorder point triggers
4. **Optimization Engine:** Multi-channel allocation, slow-mover detection
5. **PO Generator:** Draft purchase orders with recommended quantities
6. **Alert System:** Telegram bot for daily summaries + critical alerts

**Workflow:**
```
Daily 8 AM Trigger
  ↓
Pull Inventory Data (Shopify, Amazon, 3PL)
  ↓
Calculate Velocity (7d, 30d, 90d rolling averages)
  ↓
Predict Stock-Out Dates (inventory ÷ velocity)
  ↓
Compare to Reorder Points (lead time + buffer)
  ↓
Generate Alerts (Critical / Medium / Low)
  ↓
Generate Draft POs (for critical stock-outs)
  ↓
Send Telegram Summary + PO approval requests
  ↓
Log All Calculations (audit trail)
```

### 5.2 Data Sources & APIs

**Required API Access:**

| Platform | API | Purpose | Credentials Needed |
|----------|-----|---------|-------------------|
| Shopify Admin API | REST Admin API | Inventory levels, sales orders | Access tokens (11 stores) |
| Amazon SP-API | Inventory Reports | FBA inventory, sales velocity | Developer token, OAuth |
| 3PL Warehouse | Custom API or CSV | Non-FBA inventory levels | API key or SFTP access |
| Supplier Database | Internal DB or Sheets | Lead times, costs, contact info | Read access |
| Telegram Bot API | Bot API | Alert delivery, PO approval | Bot token (from BotFather) |
| Claude API | Messages API | PO draft generation, alert copy | API key |

**Data Sources:**
- **Shopify:** `inventory_items` endpoint (quantity available by location)
- **Amazon:** FBA Inventory Report (available, inbound, reserved)
- **3PL:** Luminous WMS API or daily CSV export
- **Historical Sales:** Shopify orders + Amazon orders (last 90 days for velocity)
- **Supplier Data:** Google Sheets or internal database (lead times, MOQs, costs)

### 5.3 Data Model (DuckDB Local Database)

**Tables:**

**`inventory_snapshot`** (daily snapshots)
```sql
CREATE TABLE inventory_snapshot (
  snapshot_date DATE,
  brand TEXT,
  sku TEXT,
  channel TEXT, -- 'shopify', 'amazon_fba', '3pl'
  location TEXT, -- warehouse/fulfillment center
  quantity_available INT,
  quantity_reserved INT, -- unfulfilled orders
  quantity_in_transit INT, -- POs not yet received
  quantity_total INT, -- available + reserved + in_transit
  unit_cost DECIMAL(10,2),
  PRIMARY KEY (snapshot_date, brand, sku, channel, location)
);
```

**`velocity_calculated`** (daily velocity metrics)
```sql
CREATE TABLE velocity_calculated (
  calculation_date DATE,
  brand TEXT,
  sku TEXT,
  velocity_7d DECIMAL(10,2), -- units/day (7-day avg)
  velocity_30d DECIMAL(10,2), -- units/day (30-day avg)
  velocity_90d DECIMAL(10,2), -- units/day (90-day avg)
  trend TEXT, -- 'increasing', 'stable', 'decreasing'
  seasonality_factor DECIMAL(5,2), -- 1.0 = normal, >1.0 = high season
  PRIMARY KEY (calculation_date, brand, sku)
);
```

**`stock_out_predictions`** (daily predictions)
```sql
CREATE TABLE stock_out_predictions (
  prediction_date DATE,
  brand TEXT,
  sku TEXT,
  current_inventory INT,
  velocity_used DECIMAL(10,2), -- which velocity (7d/30d/90d) was used
  predicted_stock_out_date DATE,
  days_until_stock_out INT,
  supplier_lead_time_days INT,
  reorder_point_days INT, -- lead time + safety buffer
  status TEXT, -- 'critical', 'warning', 'healthy'
  revenue_at_risk DECIMAL(10,2), -- daily revenue * days out of stock
  PRIMARY KEY (prediction_date, brand, sku)
);
```

**`reorder_recommendations`** (daily recommendations)
```sql
CREATE TABLE reorder_recommendations (
  recommendation_date DATE,
  brand TEXT,
  sku TEXT,
  recommended_quantity INT,
  rationale TEXT, -- explanation of calculation
  target_days_of_stock INT, -- desired inventory coverage
  estimated_cost DECIMAL(10,2), -- quantity * unit cost
  supplier_name TEXT,
  supplier_lead_time_days INT,
  status TEXT, -- 'pending_approval', 'approved', 'rejected', 'po_sent'
  PRIMARY KEY (recommendation_date, brand, sku)
);
```

**`purchase_orders`** (draft and approved POs)
```sql
CREATE TABLE purchase_orders (
  po_id TEXT PRIMARY KEY,
  created_date DATE,
  brand TEXT,
  supplier_name TEXT,
  line_items JSON, -- [{sku, quantity, unit_cost, total}]
  total_cost DECIMAL(10,2),
  expected_delivery_date DATE,
  status TEXT, -- 'draft', 'approved', 'sent_to_supplier', 'received'
  approved_by TEXT, -- human who approved
  approved_at TIMESTAMP,
  notes TEXT
);
```

**`slow_movers`** (weekly detection)
```sql
CREATE TABLE slow_movers (
  detection_date DATE,
  brand TEXT,
  sku TEXT,
  current_inventory INT,
  days_of_inventory INT, -- inventory / velocity
  velocity_30d DECIMAL(10,2),
  carrying_cost DECIMAL(10,2), -- storage fees + opportunity cost
  recommendation TEXT, -- 'clearance', 'bundle', 'discontinue', 'monitor'
  PRIMARY KEY (detection_date, brand, sku)
);
```

**`alert_history`** (deduplication tracking)
```sql
CREATE TABLE alert_history (
  alert_date DATE,
  brand TEXT,
  sku TEXT,
  alert_type TEXT, -- 'stock_out_critical', 'slow_mover', etc
  message_sent TEXT,
  telegram_message_id TEXT,
  PRIMARY KEY (alert_date, brand, sku, alert_type)
);
```

### 5.4 Velocity Calculation Logic

**Rolling Averages:**
```python
def calculate_velocity(sku, brand, days=7):
    """
    Calculate units sold per day over last N days.
    
    Uses Shopify + Amazon order data.
    Excludes promotional spikes (>3 std deviations from mean).
    """
    end_date = today()
    start_date = end_date - timedelta(days=days)
    
    # Pull orders from Shopify + Amazon
    orders = get_orders(brand, sku, start_date, end_date)
    
    # Sum quantities
    total_units = sum(order['quantity'] for order in orders)
    
    # Calculate daily average
    velocity = total_units / days
    
    return velocity

# Calculate 3 velocity metrics
velocity_7d = calculate_velocity(sku, brand, 7)
velocity_30d = calculate_velocity(sku, brand, 30)
velocity_90d = calculate_velocity(sku, brand, 90)
```

**Trend Detection:**
```python
def detect_trend(velocity_7d, velocity_30d, velocity_90d):
    """
    Determine if velocity is increasing, stable, or decreasing.
    """
    if velocity_7d > velocity_30d * 1.2:
        return 'increasing'  # 7-day is 20%+ higher than 30-day
    elif velocity_7d < velocity_30d * 0.8:
        return 'decreasing'  # 7-day is 20%+ lower than 30-day
    else:
        return 'stable'
```

**Which Velocity to Use:**
```python
def select_velocity(trend, velocity_7d, velocity_30d, velocity_90d):
    """
    Choose velocity metric based on trend.
    
    Increasing trend: Use 7-day (recent surge)
    Decreasing trend: Use 90-day (avoid panic)
    Stable: Use 30-day (balanced)
    """
    if trend == 'increasing':
        return velocity_7d
    elif trend == 'decreasing':
        return velocity_90d
    else:
        return velocity_30d
```

### 5.5 Stock-Out Prediction Logic

```python
def predict_stock_out(sku, brand):
    """
    Predict when SKU will run out of stock.
    """
    # Get current inventory
    inventory = get_inventory(brand, sku)
    available = inventory['quantity_available']
    reserved = inventory['quantity_reserved']
    in_transit = inventory['quantity_in_transit']
    
    # Available to sell = available - reserved (don't count reserved inventory)
    ats = available - reserved
    
    # Get velocity
    velocity_data = get_velocity(brand, sku)
    velocity = select_velocity(
        velocity_data['trend'],
        velocity_data['velocity_7d'],
        velocity_data['velocity_30d'],
        velocity_data['velocity_90d']
    )
    
    # Handle zero velocity (no recent sales)
    if velocity == 0:
        return {
            'stock_out_date': None,
            'days_until_stock_out': 9999,  # effectively infinite
            'status': 'healthy'
        }
    
    # Predict stock-out date
    days_until_stock_out = ats / velocity
    stock_out_date = today() + timedelta(days=days_until_stock_out)
    
    # Compare to reorder point
    supplier = get_supplier(brand, sku)
    lead_time = supplier['lead_time_days']
    safety_buffer = 7  # configurable per SKU
    reorder_point = lead_time + safety_buffer
    
    # Determine status
    if days_until_stock_out < lead_time:
        status = 'critical'  # URGENT: Already past reorder point
    elif days_until_stock_out < reorder_point:
        status = 'warning'  # Need to order soon
    else:
        status = 'healthy'  # Plenty of time
    
    return {
        'stock_out_date': stock_out_date,
        'days_until_stock_out': days_until_stock_out,
        'status': status,
        'velocity_used': velocity,
        'in_transit_units': in_transit  # note if PO already in transit
    }
```

### 5.6 Reorder Quantity Calculation

```python
def calculate_reorder_quantity(sku, brand):
    """
    Recommend optimal reorder quantity.
    """
    # Get velocity
    velocity = get_velocity(brand, sku)['velocity_30d']  # use 30-day for planning
    
    # Get supplier constraints
    supplier = get_supplier(brand, sku)
    lead_time = supplier['lead_time_days']
    moq = supplier['minimum_order_quantity']  # minimum order quantity
    
    # Target inventory coverage (configurable)
    target_days_of_stock = 60  # want 60 days inventory after reorder
    
    # Calculate quantity needed
    # Formula: (velocity × target days) - current inventory + (velocity × lead time)
    current_inventory = get_inventory(brand, sku)['quantity_available']
    
    # How much will we sell during lead time?
    sold_during_lead_time = velocity * lead_time
    
    # How much do we want after delivery?
    target_inventory = velocity * target_days_of_stock
    
    # Recommended quantity
    recommended = target_inventory - current_inventory + sold_during_lead_time
    
    # Apply MOQ constraint
    if recommended < moq:
        recommended = moq
    
    # Round up to case pack size (if applicable)
    case_pack = supplier.get('case_pack_size', 1)
    recommended = ceil(recommended / case_pack) * case_pack
    
    return {
        'recommended_quantity': int(recommended),
        'rationale': f"Target {target_days_of_stock}d stock, sell {sold_during_lead_time:.0f} during lead time, current inventory {current_inventory}",
        'estimated_cost': recommended * supplier['unit_cost']
    }
```

### 5.7 Multi-Channel Allocation Logic

```python
def recommend_allocation(sku, brand, total_quantity):
    """
    Recommend how to split inventory between Amazon FBA vs Shopify 3PL.
    """
    # Historical channel mix
    sales_last_90d = get_sales_by_channel(brand, sku, days=90)
    amazon_sales = sales_last_90d['amazon']
    shopify_sales = sales_last_90d['shopify']
    
    total_sales = amazon_sales + shopify_sales
    if total_sales == 0:
        # No sales history, default to 75/25 split (Wolf pattern)
        amazon_pct = 0.75
        shopify_pct = 0.25
    else:
        amazon_pct = amazon_sales / total_sales
        shopify_pct = shopify_sales / total_sales
    
    # Calculate split
    amazon_quantity = int(total_quantity * amazon_pct)
    shopify_quantity = total_quantity - amazon_quantity
    
    # Cost comparison
    fba_fee = get_fba_fee(sku)  # per-unit FBA fulfillment fee
    threePL_fee = get_3pl_fee(sku)  # per-unit 3PL fulfillment fee
    
    # Estimate total fulfillment cost
    amazon_cost = amazon_quantity * fba_fee
    shopify_cost = shopify_quantity * threePL_fee
    total_cost = amazon_cost + shopify_cost
    
    return {
        'amazon_quantity': amazon_quantity,
        'shopify_quantity': shopify_quantity,
        'amazon_pct': f"{amazon_pct*100:.1f}%",
        'shopify_pct': f"{shopify_pct*100:.1f}%",
        'estimated_fulfillment_cost': total_cost,
        'rationale': f"Based on 90-day sales mix ({amazon_pct*100:.0f}% Amazon, {shopify_pct*100:.0f}% Shopify)"
    }
```

### 5.8 Slow-Mover Detection Logic

```python
def detect_slow_movers(brand):
    """
    Flag SKUs with excessive inventory relative to velocity.
    """
    slow_movers = []
    
    for sku in get_all_skus(brand):
        # Get current inventory
        inventory = get_inventory(brand, sku)['quantity_available']
        
        # Get velocity
        velocity = get_velocity(brand, sku)['velocity_30d']
        
        # Skip if no velocity data (new product)
        if velocity == 0:
            continue
        
        # Calculate days of inventory
        days_of_inventory = inventory / velocity
        
        # Flag if >90 days inventory
        if days_of_inventory > 90:
            # Calculate carrying cost
            unit_cost = get_cost(brand, sku)
            total_value = inventory * unit_cost
            
            # Amazon FBA storage fees (example: $0.75/cu ft/month)
            storage_fee = calculate_storage_fee(sku, inventory)
            
            # Opportunity cost (tie up cash)
            opportunity_cost = total_value * 0.01  # 1% monthly
            
            carrying_cost = storage_fee + opportunity_cost
            
            # Recommend action
            if days_of_inventory > 180:
                recommendation = 'discontinue'  # 6+ months = dead product
            elif days_of_inventory > 120:
                recommendation = 'clearance'  # 4+ months = aggressive discount
            else:
                recommendation = 'bundle'  # 3+ months = bundle with fast-mover
            
            slow_movers.append({
                'sku': sku,
                'current_inventory': inventory,
                'days_of_inventory': int(days_of_inventory),
                'total_value': total_value,
                'carrying_cost': carrying_cost,
                'recommendation': recommendation
            })
    
    return sorted(slow_movers, key=lambda x: x['days_of_inventory'], reverse=True)
```

---

## 6. Implementation Phases

### Phase 1: Data Foundation (Days 1-2, March 6-7)

**Deliverables:**
- [ ] Set up DuckDB local database
- [ ] Create 7 tables (inventory_snapshot, velocity_calculated, stock_out_predictions, reorder_recommendations, purchase_orders, slow_movers, alert_history)
- [ ] Build Shopify inventory ingestion (11 stores)
- [ ] Build Amazon FBA inventory ingestion (SP-API)
- [ ] Build 3PL inventory ingestion (Luminous WMS or CSV)
- [ ] Test data pipeline (pull data for Wolf Tactical, verify accuracy)

**Milestone:** Can pull complete inventory snapshot for Wolf Tactical from all sources

---

### Phase 2: Velocity Engine (Days 3-4, March 8-9)

**Deliverables:**
- [ ] Build velocity calculation engine (7d, 30d, 90d rolling averages)
- [ ] Build trend detection (increasing/stable/decreasing)
- [ ] Build velocity selection logic (which average to use)
- [ ] Test on Wolf Tactical historical data (validate against known stock-outs)
- [ ] Backtest predictions (would we have caught Feb stock-outs?)

**Milestone:** Velocity calculations accurate within 10% of actual sales patterns

---

### Phase 3: Prediction Engine (Days 5-7, March 10-12)

**Deliverables:**
- [ ] Build stock-out prediction logic (inventory ÷ velocity = days until out)
- [ ] Build reorder point calculation (lead time + safety buffer)
- [ ] Build alert classification (critical/warning/healthy)
- [ ] Build revenue-at-risk calculation (daily revenue × days out of stock)
- [ ] Test on Wolf Tactical (generate today's alerts)
- [ ] Validate with Dustin/Bilal (do alerts make sense?)

**Milestone:** Stock-out predictions tested and validated with real Wolf data

---

### Phase 4: PO Generation + Alerts (Days 8-10, March 13-15)

**Deliverables:**
- [ ] Build reorder quantity calculator (target days of stock formula)
- [ ] Build draft PO generator (SKU, quantity, supplier, cost)
- [ ] Build Telegram bot integration (daily summaries + critical alerts)
- [ ] Build PO approval workflow (Telegram buttons: Approve / Reject / Modify)
- [ ] Test alert delivery (send test alerts to Dustin's Telegram)
- [ ] Test PO approval flow (approve draft PO, verify logging)

**Milestone:** Daily alerts + draft POs delivered to Telegram, approval workflow operational

---

### Phase 5: Optimization Features (Days 11-12, March 16-17)

**Deliverables:**
- [ ] Build multi-channel allocation optimizer (Amazon vs Shopify split)
- [ ] Build slow-mover detection (>90 days inventory flagging)
- [ ] Build carrying cost calculator (storage fees + opportunity cost)
- [ ] Build clearance recommendations (pricing, bundling, discontinuation)
- [ ] Test on Wolf Tactical (identify current slow-movers)
- [ ] Generate first weekly slow-mover report

**Milestone:** Full feature set operational, tested on Wolf Tactical

---

### Phase 6: Scale to 13 Brands (Days 13-14, March 18-19)

**Deliverables:**
- [ ] Add remaining 10 Society Brands to system
- [ ] Configure supplier data for all brands
- [ ] Configure lead times for all SKUs
- [ ] Test multi-brand daily run (all 11 brands processed in <10 minutes)
- [ ] Document agent operations (how to interpret alerts, approve POs)
- [ ] Deliver final agent to Dustin

**Milestone:** Agent operational across Society Brands portfolio

---

## 7. Success Metrics & KPIs

### Operational Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Stock-out prediction accuracy | >90% | Predicted date within 3 days of actual |
| False negative rate | 0% | Zero missed critical stock-outs |
| Alert noise | <5 critical/day | Only true urgencies trigger critical alerts |
| Reorder quantity accuracy | Within 10% | Recommended vs actual optimal |
| Multi-channel allocation savings | 5%+ | Fulfillment cost reduction |
| Slow-mover detection rate | 100% | All >120d inventory flagged |

### Business Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Stock-out incident reduction | -80% | vs baseline (manual forecasting) |
| Overstock reduction | -30% | Total inventory value tied up |
| FBA storage fee reduction | -20% | Long-term storage fees avoided |
| Time spent on forecasting | -95% | Manual spreadsheet hours eliminated |
| Cash flow improvement | +15% | Free up cash from excess inventory |

---

## 8. Risk Management

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Shopify API rate limits | High | Medium | Cache data, batch requests, exponential backoff |
| Amazon API delays (24h lag) | Medium | High | Use yesterday's data, note lag in alerts |
| Velocity spikes from promos | High | Medium | Exclude outliers (>3 std dev), promotional calendar integration |
| 3PL API unavailable | High | Low | Fallback to CSV import, alert if data stale |
| DuckDB performance at scale | Medium | Low | Optimize queries, add indexes, test with 1M+ records |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Agent recommends wrong quantity | High | Low | Human approves all POs, log all calculations for audit |
| Missed critical stock-out | High | Low | Multiple velocity metrics, conservative buffers, backtesting |
| Alert fatigue (too many) | Medium | Medium | Tune thresholds, batch non-critical alerts |
| Supplier lead time changes | Medium | High | Track actual vs expected delivery, update lead times |
| Seasonal demand spike | High | Medium | Historical seasonality factors, promotional calendar integration |

---

## 9. Dependencies & Prerequisites

**Before Starting Build:**

**Shopify:**
- [ ] Admin API access tokens (11 stores)
- [ ] Inventory read permissions verified

**Amazon:**
- [ ] SP-API credentials (all brands)
- [ ] FBA Inventory Reports access
- [ ] Test with one brand first (Wolf Tactical)

**3PL Warehouse:**
- [ ] Luminous WMS API access OR
- [ ] Daily CSV export set up (SFTP or email)

**Supplier Data:**
- [ ] Google Sheet or database with:
  - Supplier names
  - Lead times (days)
  - Minimum order quantities (MOQs)
  - Unit costs
  - Contact info

**Infrastructure:**
- [ ] Python 3.10+ environment
- [ ] DuckDB installed
- [ ] Claude API key available
- [ ] Telegram bot created (token from BotFather)

---

## 10. Teikametrics Alternative (Buy vs Build Decision)

**Teikametrics offers inventory forecasting module. Should we buy instead of build?**

### Build Pros:
- ✅ Full customization (multi-channel allocation, slow-mover detection, Society Brands portfolio logic)
- ✅ Own the data (no vendor lock-in)
- ✅ Integrate with other agents (Amazon Agent, Financial Agent)
- ✅ Lower ongoing cost (no monthly subscription)
- ✅ Fast iteration (add features as needed)

### Build Cons:
- ❌ 1-2 weeks development time
- ❌ Maintenance burden (bugs, API changes)
- ❌ Must build expertise in inventory management

### Buy (Teikametrics) Pros:
- ✅ Instant availability (no build time)
- ✅ Proven accuracy (used by 1000s of Amazon sellers)
- ✅ No maintenance burden
- ✅ Built-in Amazon Ads integration

### Buy (Teikametrics) Cons:
- ❌ Monthly subscription cost ($?? — need pricing)
- ❌ Limited customization (can't add multi-brand logic)
- ❌ Amazon-only (doesn't handle Shopify 3PL allocation)
- ❌ Vendor lock-in (can't port to other platforms)

### Recommendation:
**Build** if:
- Teikametrics pricing >$500/month
- Need multi-channel optimization (Shopify + Amazon)
- Want Society Brands portfolio features (13-brand scale)

**Buy (Teikametrics)** if:
- Teikametrics pricing <$300/month
- Amazon-only forecasting sufficient (not Shopify)
- Want instant availability (can't wait 1-2 weeks)

**Hybrid:**
- Use Teikametrics for Amazon FBA forecasting
- Build Shopify 3PL forecasting in-house
- Integrate both via this agent (pull Teikametrics recommendations, combine with Shopify data)

---

## 11. Integration with Milan's Amazon Agent

**Inventory forecasting was originally part of Amazon Agent roadmap (Dustin + Carla discussion).**

**Milan's Amazon Agent includes:**
- ✅ Stranded inventory monitoring (reactive: inventory already stuck)
- ✅ Out-of-stock alerts (reactive: already out)

**This Inventory Agent adds:**
- 🆕 Predictive stock-out alerts (BEFORE running out)
- 🆕 Reorder quantity recommendations
- 🆕 Multi-channel allocation (Amazon vs Shopify)

**Integration Points:**
1. **Share inventory data:** Milan's agent pulls Amazon FBA inventory → feed to this agent
2. **Share alerts:** Milan's agent detects Buy Box loss from stock-out → trigger this agent's reorder workflow
3. **Unified Telegram alerts:** Both agents send to same channel, coordinated severity levels

**Decision:** Build as separate agent OR extend Milan's Amazon Agent?
- **Separate Agent Pros:** Faster build (no coordination with Milan), handles Shopify + Amazon + 3PL
- **Extend Milan's Agent Pros:** Unified Amazon operations (health + inventory + ads)

**Recommendation:** Build as **separate Inventory Agent** for speed, integrate via shared data sources.

---

## 12. Handoff Checklist

### Charles's Responsibilities:
- [ ] Review this plan control document v1.0
- [ ] Set up development environment (Python, DuckDB, APIs)
- [ ] Build Phase 1-6 (12-14 days)
- [ ] Test on Wolf Tactical
- [ ] Scale to 13 brands
- [ ] Document agent operations
- [ ] Deliver runbook to Dustin

### Dustin's Responsibilities:
- [ ] Approve this plan v1.0
- [ ] Provide Shopify API tokens (11 stores)
- [ ] Provide Amazon SP-API credentials
- [ ] Provide 3PL inventory data access (Luminous)
- [ ] Provide supplier data (Google Sheet or database)
- [ ] Test Phase 3 alerts (validate predictions make sense)
- [ ] Approve/reject draft POs during Phase 4 testing
- [ ] Decide: Build vs buy Teikametrics (provide pricing if available)

### Carla's Responsibilities:
- [ ] Provide supplier lead time data
- [ ] Validate reorder quantity recommendations
- [ ] Review slow-mover clearance recommendations

---

## 13. Contact & Escalation

**Project Owner:** Dustin Brode  
**Communication Channel:** Telegram (7099780243)

**Escalation Path:**
1. Charles encounters blocker → Message Dustin in Telegram
2. Technical questions → Tag Dustin for clarification
3. Business decisions (supplier data, lead times, MOQs) → Dustin + Carla
4. Integration with Milan's Amazon Agent → Coordinate with Milan

---

## 14. Documentation Deliverables

**Charles must provide:**

**Technical Documentation:**
- Database schema (7 tables with column definitions)
- API integration guide (Shopify, Amazon, 3PL)
- Calculation logic (velocity, stock-out prediction, reorder quantity)
- Alert classification logic (critical/warning/healthy)

**User Documentation:**
- Alert interpretation guide (what each alert means)
- PO approval procedures (how to review, approve, reject)
- Slow-mover action guide (clearance, bundling, discontinuation)
- Troubleshooting runbook

**Audit Trail:**
- All calculations logged to database
- All alerts logged with timestamps
- All PO approvals/rejections logged
- Sample alerts (critical/medium/low examples)

---

## 15. Acceptance Criteria

**Project is complete when:**

✅ Agent operational for Wolf Tactical (11 SKUs+ monitored daily)  
✅ Daily stock-out alerts delivered to Telegram with accurate predictions  
✅ Reorder quantity recommendations accurate within 10%  
✅ Draft POs generated with supplier info, costs, lead times  
✅ PO approval workflow operational (Telegram buttons work)  
✅ Multi-channel allocation recommendations save 5%+ on fulfillment costs  
✅ Slow-mover detection flags 100% of SKUs with >120 days inventory  
✅ Zero false negatives on critical stock-outs (tested on historical data)  
✅ System scales to 13 brands without performance issues  
✅ Documentation complete (technical + user guides)  
✅ Dustin signs off after 1-week live test  

---

## Appendix A: Supplier Data Template

**Google Sheet Format:**

| Brand | SKU | Supplier Name | Lead Time (Days) | MOQ | Unit Cost | Case Pack | Contact Email |
|-------|-----|---------------|------------------|-----|-----------|-----------|---------------|
| Wolf Tactical | B08XYZ | Acme Manufacturing | 14 | 100 | $12.50 | 50 | orders@acme.com |
| Wolf Tactical | B07ABC | Beta Suppliers | 21 | 200 | $8.75 | 100 | sales@beta.com |

**Required Fields:**
- **Lead Time:** Days from PO submission to warehouse receipt
- **MOQ:** Minimum order quantity
- **Unit Cost:** Cost per unit (for PO value calculation)
- **Case Pack:** Units per case (for rounding recommendations)

---

## Appendix B: Example Daily Alert

**Telegram Message:**
```
📦 Wolf Tactical Inventory Alert (March 6, 2026)

🚨 URGENT REORDERS (3):

1. Tactical Pants (B08XYZ123)
   • Stock-out in: 8 days
   • Lead time: 14 days
   • Revenue at risk: $2,100/day
   • Current inventory: 47 units
   • Velocity: 5.9 units/day
   • Recommendation: Order 500 units ($6,250 total)
   [View Draft PO] [Approve] [Reject]

2. Tactical Belt (B07DEF456)
   • Stock-out in: 10 days
   • Lead time: 21 days
   • Revenue at risk: $1,400/day
   • Current inventory: 62 units
   • Velocity: 6.2 units/day
   • Recommendation: Order 300 units ($3,900 total)
   [View Draft PO] [Approve] [Reject]

3. Tactical Vest (B06GHI789)
   • Stock-out in: 12 days
   • Lead time: 14 days
   • Revenue at risk: $900/day
   • Current inventory: 38 units
   • Velocity: 3.2 units/day
   • Recommendation: Order 200 units ($4,500 total)
   [View Draft PO] [Approve] [Reject]

⚠️ UPCOMING REORDERS (5):
• Tactical Gloves (18 days)
• Tactical Backpack (22 days)
• [3 more...]

✅ HEALTHY INVENTORY: 47 SKUs

[View Full Report]
```

---

**END OF PLAN CONTROL DOCUMENT**

**Status:** Ready for Dustin's approval  
**Next Step:** Approve plan → Charles starts Phase 1 (Data Foundation)  
**Target Completion:** March 17, 2026 (12 days)
