-- Inventory Forecasting Agent Database Schema
-- Created: March 7, 2026 (Phase 1, Day 1)
-- Database: society_brands_local.db
-- Purpose: Predictive stock-out alerts + reorder recommendations

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- 1. Inventory Snapshot (Daily inventory levels across all channels)
CREATE TABLE IF NOT EXISTS inventory_snapshot (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date DATE NOT NULL,
    brand TEXT NOT NULL,
    sku TEXT NOT NULL,
    product_title TEXT,
    variant_title TEXT,
    
    -- Shopify Inventory
    shopify_available INTEGER DEFAULT 0,
    shopify_committed INTEGER DEFAULT 0,
    shopify_incoming INTEGER DEFAULT 0,
    shopify_location TEXT,
    
    -- Amazon FBA Inventory
    amazon_fba_available INTEGER DEFAULT 0,
    amazon_fba_inbound INTEGER DEFAULT 0,
    amazon_fba_reserved INTEGER DEFAULT 0,
    amazon_fba_unfulfillable INTEGER DEFAULT 0,
    
    -- Totals
    total_available INTEGER GENERATED ALWAYS AS (shopify_available + amazon_fba_available) STORED,
    total_incoming INTEGER GENERATED ALWAYS AS (shopify_incoming + amazon_fba_inbound) STORED,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(snapshot_date, brand, sku)
);

CREATE INDEX idx_inventory_snapshot_brand_sku ON inventory_snapshot(brand, sku);
CREATE INDEX idx_inventory_snapshot_date ON inventory_snapshot(snapshot_date);

-- 2. Sales Velocity (7-day, 30-day, 90-day rolling averages)
CREATE TABLE IF NOT EXISTS sales_velocity (
    velocity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    calculation_date DATE NOT NULL,
    brand TEXT NOT NULL,
    sku TEXT NOT NULL,
    
    -- Velocity Calculations
    velocity_7d REAL DEFAULT 0,    -- Units per day (7-day average)
    velocity_30d REAL DEFAULT 0,   -- Units per day (30-day average)
    velocity_90d REAL DEFAULT 0,   -- Units per day (90-day average)
    
    -- Trend Analysis
    trend_7d_vs_30d REAL,          -- % change
    trend_30d_vs_90d REAL,         -- % change
    is_accelerating BOOLEAN,       -- TRUE if velocity increasing
    
    -- Sales Data
    units_sold_7d INTEGER DEFAULT 0,
    units_sold_30d INTEGER DEFAULT 0,
    units_sold_90d INTEGER DEFAULT 0,
    revenue_7d REAL DEFAULT 0,
    revenue_30d REAL DEFAULT 0,
    revenue_90d REAL DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(calculation_date, brand, sku)
);

CREATE INDEX idx_sales_velocity_brand_sku ON sales_velocity(brand, sku);
CREATE INDEX idx_sales_velocity_date ON sales_velocity(calculation_date);

-- 3. Stock-Out Predictions (Days until out-of-stock)
CREATE TABLE IF NOT EXISTS stockout_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_date DATE NOT NULL,
    brand TEXT NOT NULL,
    sku TEXT NOT NULL,
    product_title TEXT,
    
    -- Current State
    current_inventory INTEGER NOT NULL,
    incoming_inventory INTEGER DEFAULT 0,
    
    -- Velocity-Based Prediction
    velocity_used TEXT NOT NULL,   -- '7d', '30d', '90d', or 'adaptive'
    daily_velocity REAL NOT NULL,
    days_until_stockout INTEGER,   -- NULL = >365 days
    stockout_date DATE,             -- NULL = >365 days out
    
    -- Risk Classification
    risk_level TEXT CHECK(risk_level IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE')),
    -- CRITICAL: <7 days
    -- HIGH: 7-14 days
    -- MEDIUM: 14-30 days
    -- LOW: 30-60 days
    -- NONE: >60 days
    
    -- Confidence Metrics
    prediction_confidence REAL,    -- 0.0-1.0 (based on velocity stability)
    velocity_variance REAL,        -- Standard deviation of daily sales
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(prediction_date, brand, sku)
);

CREATE INDEX idx_stockout_predictions_risk ON stockout_predictions(risk_level);
CREATE INDEX idx_stockout_predictions_brand_sku ON stockout_predictions(brand, sku);
CREATE INDEX idx_stockout_predictions_date ON stockout_predictions(stockout_date);

-- 4. Reorder Recommendations (Draft POs with MOQ/lead time)
CREATE TABLE IF NOT EXISTS reorder_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_date DATE NOT NULL,
    brand TEXT NOT NULL,
    sku TEXT NOT NULL,
    product_title TEXT,
    
    -- Recommendation Details
    recommended_quantity INTEGER NOT NULL,
    reorder_urgency TEXT CHECK(reorder_urgency IN ('URGENT', 'HIGH', 'MEDIUM', 'LOW')),
    -- URGENT: <7 days until stockout
    -- HIGH: 7-14 days
    -- MEDIUM: 14-30 days
    -- LOW: Safety stock replenishment
    
    -- Supplier Information
    supplier_name TEXT,
    moq INTEGER,                    -- Minimum Order Quantity
    lead_time_days INTEGER,
    cost_per_unit REAL,
    
    -- Financial Calculation
    order_cost REAL,                -- recommended_quantity * cost_per_unit
    expected_revenue REAL,          -- Based on velocity * selling price
    expected_profit REAL,           -- expected_revenue - order_cost
    
    -- Allocation Strategy
    allocation_shopify INTEGER,
    allocation_amazon INTEGER,
    allocation_reasoning TEXT,
    
    -- Action Tracking
    status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'REVIEWED', 'APPROVED', 'ORDERED', 'REJECTED')),
    reviewed_by TEXT,
    reviewed_at TIMESTAMP,
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reorder_recommendations_brand_sku ON reorder_recommendations(brand, sku);
CREATE INDEX idx_reorder_recommendations_urgency ON reorder_recommendations(reorder_urgency);
CREATE INDEX idx_reorder_recommendations_status ON reorder_recommendations(status);

-- 5. Slow Movers (>90 days inventory, liquidation candidates)
CREATE TABLE IF NOT EXISTS slow_movers (
    slow_mover_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_date DATE NOT NULL,
    brand TEXT NOT NULL,
    sku TEXT NOT NULL,
    product_title TEXT,
    
    -- Inventory Analysis
    current_inventory INTEGER NOT NULL,
    days_of_inventory INTEGER NOT NULL,  -- current_inventory / daily_velocity
    total_inventory_value REAL,          -- current_inventory * cost_per_unit
    
    -- Sales Performance
    units_sold_90d INTEGER DEFAULT 0,
    daily_velocity REAL,
    last_sale_date DATE,
    days_since_last_sale INTEGER,
    
    -- Recommendation
    action_recommended TEXT CHECK(action_recommended IN ('LIQUIDATE', 'DISCOUNT', 'BUNDLE', 'MONITOR', 'REMOVE')),
    -- LIQUIDATE: >180 days inventory, sell at cost
    -- DISCOUNT: >120 days inventory, 30-50% off
    -- BUNDLE: >90 days inventory, include in bundles
    -- MONITOR: 60-90 days inventory, watch closely
    -- REMOVE: Dead SKU, remove from catalog
    
    suggested_discount_pct INTEGER,
    estimated_recovery_value REAL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(analysis_date, brand, sku)
);

CREATE INDEX idx_slow_movers_brand_sku ON slow_movers(brand, sku);
CREATE INDEX idx_slow_movers_action ON slow_movers(action_recommended);
CREATE INDEX idx_slow_movers_days ON slow_movers(days_of_inventory);

-- 6. Agent Execution Log (Audit trail for all agent actions)
CREATE TABLE IF NOT EXISTS inventory_agent_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_date DATE NOT NULL,
    execution_type TEXT NOT NULL CHECK(execution_type IN ('SNAPSHOT', 'VELOCITY', 'PREDICTION', 'RECOMMENDATION', 'ANALYSIS', 'ALERT')),
    
    -- Execution Metrics
    brands_processed INTEGER,
    skus_processed INTEGER,
    records_created INTEGER,
    records_updated INTEGER,
    
    -- Alerts Generated
    critical_alerts INTEGER DEFAULT 0,
    high_alerts INTEGER DEFAULT 0,
    medium_alerts INTEGER DEFAULT 0,
    
    -- Performance
    execution_duration_seconds INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inventory_agent_log_date ON inventory_agent_log(execution_date);
CREATE INDEX idx_inventory_agent_log_type ON inventory_agent_log(execution_type);

-- 7. Product Master (SKU metadata for lookups)
CREATE TABLE IF NOT EXISTS product_master (
    sku TEXT PRIMARY KEY,
    brand TEXT NOT NULL,
    product_title TEXT,
    variant_title TEXT,
    
    -- Supplier Info
    supplier_name TEXT,
    moq INTEGER,
    lead_time_days INTEGER,
    cost_per_unit REAL,
    
    -- Pricing
    retail_price REAL,
    wholesale_price REAL,
    
    -- Category
    product_type TEXT,
    is_consumable BOOLEAN DEFAULT FALSE,
    is_seasonal BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    discontinuation_date DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_master_brand ON product_master(brand);
CREATE INDEX idx_product_master_active ON product_master(is_active);

-- ============================================================================
-- VIEWS FOR QUICK ACCESS
-- ============================================================================

-- Current Stock Status (Latest snapshot + prediction)
CREATE VIEW IF NOT EXISTS v_current_stock_status AS
SELECT 
    i.brand,
    i.sku,
    i.product_title,
    i.total_available as current_inventory,
    i.total_incoming as incoming_inventory,
    v.velocity_30d as daily_velocity,
    p.days_until_stockout,
    p.stockout_date,
    p.risk_level,
    p.prediction_confidence,
    i.snapshot_date,
    p.prediction_date
FROM inventory_snapshot i
LEFT JOIN sales_velocity v ON i.brand = v.brand AND i.sku = v.sku AND v.calculation_date = i.snapshot_date
LEFT JOIN stockout_predictions p ON i.brand = p.brand AND i.sku = p.sku AND p.prediction_date = i.snapshot_date
WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshot)
ORDER BY p.risk_level DESC, p.days_until_stockout ASC;

-- Critical Reorders Needed
CREATE VIEW IF NOT EXISTS v_critical_reorders AS
SELECT 
    r.brand,
    r.sku,
    r.product_title,
    r.recommended_quantity,
    r.reorder_urgency,
    r.order_cost,
    r.expected_profit,
    r.supplier_name,
    r.lead_time_days,
    p.days_until_stockout,
    r.status,
    r.recommendation_date
FROM reorder_recommendations r
LEFT JOIN stockout_predictions p ON r.brand = p.brand AND r.sku = p.sku 
    AND p.prediction_date = r.recommendation_date
WHERE r.status = 'PENDING'
ORDER BY r.reorder_urgency DESC, p.days_until_stockout ASC;

-- Slow Mover Summary by Brand
CREATE VIEW IF NOT EXISTS v_slow_mover_summary AS
SELECT 
    brand,
    action_recommended,
    COUNT(*) as sku_count,
    SUM(current_inventory) as total_units,
    SUM(total_inventory_value) as total_value,
    SUM(estimated_recovery_value) as recovery_value
FROM slow_movers
WHERE analysis_date = (SELECT MAX(analysis_date) FROM slow_movers)
GROUP BY brand, action_recommended
ORDER BY brand, total_value DESC;

-- ============================================================================
-- INITIAL DATA COMMENT
-- ============================================================================

-- Next Steps:
-- 1. Run extract_shopify_inventory.py to populate inventory_snapshot
-- 2. Run calculate_sales_velocity.py to populate sales_velocity
-- 3. Run predict_stockouts.py to populate stockout_predictions
-- 4. Run generate_reorder_recommendations.py to populate reorder_recommendations
-- 5. Run identify_slow_movers.py to populate slow_movers
