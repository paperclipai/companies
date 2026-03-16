#!/usr/bin/env python3
"""
Sales Velocity Calculator for Inventory Forecasting Agent
Created: March 7, 2026 (Phase 1, Day 1)

Purpose: Calculate 7-day, 30-day, 90-day rolling sales velocity per SKU

Data Source: Definite SHOPIFY.order_line_items (historical order data)

Calculations:
- velocity_7d = units_sold_last_7_days / 7
- velocity_30d = units_sold_last_30_days / 30
- velocity_90d = units_sold_last_90_days / 90
- trend_7d_vs_30d = (velocity_7d - velocity_30d) / velocity_30d * 100
- is_accelerating = trend_7d_vs_30d > 10%
"""

import sqlite3
import requests
from datetime import datetime, date, timedelta
import os
import sys
import statistics

# Configuration
DATABASE_PATH = os.path.expanduser("~/clawd/workstreams/database-setup/society_brands_local.db")
DEFINITE_API_KEY = "acb226c2489e4e5c8ba43c92b5153829-SvrhStC3utT0JSuEgULdLH7bngvQKR9h"
DEFINITE_API_BASE = "https://api.definite.app/v1"

def log(message, level="INFO"):
    """Simple logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def query_definite(sql):
    """Query Definite API"""
    headers = {"Authorization": f"Bearer {DEFINITE_API_KEY}"}
    payload = {"sql": sql}
    
    try:
        response = requests.post(f"{DEFINITE_API_BASE}/query", json=payload, headers=headers, timeout=180)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        log(f"Definite API error: {e}", "ERROR")
        return []

def extract_sales_velocity_data():
    """
    Extract order line items for velocity calculation
    
    Strategy:
    1. Pull last 90 days of order_line_items
    2. Group by SKU + time period (7d, 30d, 90d)
    3. Calculate units sold + revenue per period
    """
    log("Extracting sales data from Definite...")
    
    today = date.today()
    date_90d_ago = today - timedelta(days=90)
    date_30d_ago = today - timedelta(days=30)
    date_7d_ago = today - timedelta(days=7)
    
    # Query all order line items from last 90 days
    sql = f"""
    SELECT 
        CASE 
            WHEN oli.sku LIKE 'AC-%' THEN 'Active Charis'
            WHEN oli.sku LIKE 'CLF-%' THEN 'Clarifion'
            WHEN oli.sku LIKE 'CAPSULE-%' OR oli.sku LIKE 'CS-%' THEN 'PureCaps USA'
            WHEN oli.sku LIKE 'CLN-%' THEN 'Cleanomic'
            WHEN oli.sku LIKE 'CEB-%' THEN 'Club EarlyBird'
            WHEN oli.sku LIKE 'CRN-%' OR oli.sku LIKE 'CRUNCHI-%' THEN 'Crunchi'
            WHEN oli.sku LIKE 'DNKE-%' THEN 'Damn Near Kilt Em'
            WHEN oli.sku LIKE 'PLO-%' THEN 'Primal Life Organics'
            WHEN oli.sku LIKE 'PT-%' THEN 'Power Theory'
            WHEN oli.sku LIKE 'WOLF-%' OR oli.sku LIKE 'WT-%' THEN 'Wolf Tactical'
            WHEN oli.sku LIKE 'YTB-%' THEN 'Yankee Toybox'
            ELSE 'Unknown'
        END as brand,
        oli.sku,
        oli.name as product_name,
        DATE(o.created_at) as order_date,
        oli.quantity,
        oli.price * oli.quantity as revenue
    FROM SHOPIFY.order_line_items oli
    JOIN SHOPIFY.orders o ON oli.order_id = o.id
    WHERE o.created_at >= '{date_90d_ago}'
        AND o.financial_status IN ('paid', 'partially_paid')
        AND o.fulfillment_status != 'refunded'
        AND oli.sku IS NOT NULL
        AND oli.sku != ''
        AND oli.quantity > 0
    ORDER BY oli.sku, order_date DESC
    """
    
    results = query_definite(sql)
    log(f"Retrieved {len(results)} order line items (90 days)")
    
    return results, date_7d_ago, date_30d_ago, date_90d_ago

def calculate_velocity_for_sku(orders, sku, date_7d, date_30d, date_90d):
    """Calculate velocity metrics for a single SKU"""
    sku_orders = [o for o in orders if o['sku'] == sku]
    
    if not sku_orders:
        return None
    
    # Parse dates
    def parse_date(d):
        if isinstance(d, str):
            return datetime.strptime(d.split('T')[0], '%Y-%m-%d').date()
        return d
    
    # Calculate units sold by period
    units_7d = sum(o['quantity'] for o in sku_orders if parse_date(o['order_date']) >= date_7d)
    units_30d = sum(o['quantity'] for o in sku_orders if parse_date(o['order_date']) >= date_30d)
    units_90d = sum(o['quantity'] for o in sku_orders if parse_date(o['order_date']) >= date_90d)
    
    revenue_7d = sum(o['revenue'] for o in sku_orders if parse_date(o['order_date']) >= date_7d)
    revenue_30d = sum(o['revenue'] for o in sku_orders if parse_date(o['order_date']) >= date_30d)
    revenue_90d = sum(o['revenue'] for o in sku_orders if parse_date(o['order_date']) >= date_90d)
    
    # Calculate daily velocity
    velocity_7d = units_7d / 7 if units_7d > 0 else 0
    velocity_30d = units_30d / 30 if units_30d > 0 else 0
    velocity_90d = units_90d / 90 if units_90d > 0 else 0
    
    # Trend analysis
    trend_7d_vs_30d = None
    trend_30d_vs_90d = None
    is_accelerating = False
    
    if velocity_30d > 0:
        trend_7d_vs_30d = ((velocity_7d - velocity_30d) / velocity_30d) * 100
        if trend_7d_vs_30d > 10:
            is_accelerating = True
    
    if velocity_90d > 0:
        trend_30d_vs_90d = ((velocity_30d - velocity_90d) / velocity_90d) * 100
    
    return {
        'brand': sku_orders[0]['brand'],
        'sku': sku,
        'velocity_7d': round(velocity_7d, 2),
        'velocity_30d': round(velocity_30d, 2),
        'velocity_90d': round(velocity_90d, 2),
        'trend_7d_vs_30d': round(trend_7d_vs_30d, 2) if trend_7d_vs_30d is not None else None,
        'trend_30d_vs_90d': round(trend_30d_vs_90d, 2) if trend_30d_vs_90d is not None else None,
        'is_accelerating': is_accelerating,
        'units_sold_7d': units_7d,
        'units_sold_30d': units_30d,
        'units_sold_90d': units_90d,
        'revenue_7d': round(revenue_7d, 2),
        'revenue_30d': round(revenue_30d, 2),
        'revenue_90d': round(revenue_90d, 2)
    }

def insert_velocity_records(conn, calculation_date, velocity_records):
    """Insert velocity records into sales_velocity table"""
    cursor = conn.cursor()
    
    inserted = 0
    for record in velocity_records:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO sales_velocity (
                    calculation_date, brand, sku,
                    velocity_7d, velocity_30d, velocity_90d,
                    trend_7d_vs_30d, trend_30d_vs_90d, is_accelerating,
                    units_sold_7d, units_sold_30d, units_sold_90d,
                    revenue_7d, revenue_30d, revenue_90d
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                calculation_date,
                record['brand'],
                record['sku'],
                record['velocity_7d'],
                record['velocity_30d'],
                record['velocity_90d'],
                record['trend_7d_vs_30d'],
                record['trend_30d_vs_90d'],
                record['is_accelerating'],
                record['units_sold_7d'],
                record['units_sold_30d'],
                record['units_sold_90d'],
                record['revenue_7d'],
                record['revenue_30d'],
                record['revenue_90d']
            ))
            inserted += 1
        except sqlite3.Error as e:
            log(f"Error inserting velocity for SKU {record['sku']}: {e}", "ERROR")
    
    conn.commit()
    log(f"Inserted {inserted} velocity records")
    return inserted

def log_execution(conn, execution_type, brands_processed, skus_processed, records_created, duration, success=True, error_msg=None):
    """Log agent execution to inventory_agent_log table"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory_agent_log (
            execution_date, execution_type, brands_processed, skus_processed,
            records_created, execution_duration_seconds, success, error_message
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        date.today(), execution_type, brands_processed, skus_processed,
        records_created, duration, success, error_msg
    ))
    conn.commit()

def main():
    """Main execution"""
    start_time = datetime.now()
    log("Starting sales velocity calculation...")
    
    try:
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        log(f"Connected to database: {DATABASE_PATH}")
        
        # Extract sales data
        orders, date_7d, date_30d, date_90d = extract_sales_velocity_data()
        
        if not orders:
            log("No order data found", "WARNING")
            log_execution(conn, 'VELOCITY', 0, 0, 0, 0, False, "No orders from Definite")
            return
        
        # Get unique SKUs
        unique_skus = list(set(o['sku'] for o in orders))
        log(f"Calculating velocity for {len(unique_skus)} SKUs...")
        
        # Calculate velocity for each SKU
        velocity_records = []
        for i, sku in enumerate(unique_skus):
            if i % 100 == 0 and i > 0:
                log(f"  Progress: {i}/{len(unique_skus)} SKUs processed")
            
            velocity = calculate_velocity_for_sku(orders, sku, date_7d, date_30d, date_90d)
            if velocity:
                velocity_records.append(velocity)
        
        log(f"Calculated velocity for {len(velocity_records)} SKUs")
        
        # Count unique brands
        brands = set(r['brand'] for r in velocity_records)
        
        # Insert velocity records
        today = date.today()
        records_created = insert_velocity_records(conn, today, velocity_records)
        
        # Log execution
        duration = int((datetime.now() - start_time).total_seconds())
        log_execution(conn, 'VELOCITY', len(brands), len(velocity_records), records_created, duration, True, None)
        
        log(f"✅ Velocity calculation complete in {duration}s")
        
        # Summary stats
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                brand,
                COUNT(*) as sku_count,
                AVG(velocity_30d) as avg_velocity,
                SUM(CASE WHEN is_accelerating THEN 1 ELSE 0 END) as accelerating_count
            FROM sales_velocity
            WHERE calculation_date = ?
            GROUP BY brand
            ORDER BY avg_velocity DESC
        """, (today,))
        
        log("\n📊 Velocity Summary:")
        for row in cursor.fetchall():
            log(f"  {row[0]}: {row[1]} SKUs, avg {row[2]:.2f} units/day, {row[3]} accelerating")
        
        conn.close()
        
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        duration = int((datetime.now() - start_time).total_seconds())
        try:
            log_execution(conn, 'VELOCITY', 0, 0, 0, duration, False, str(e))
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
