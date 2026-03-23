#!/usr/bin/env python3
"""
Shopify Inventory Sync for Inventory Forecasting Agent
Created: March 7, 2026 (Phase 1, Day 1)

Purpose: Pull current inventory levels from all 11 Shopify stores into inventory_snapshot table

Data Sources:
1. PRIMARY: Shopify Admin API (11 stores) - BLOCKED (need API tokens)
2. FALLBACK: Definite SHOPIFY.inventory_levels table (existing data)

Phase 1 Implementation: Use Definite fallback until Shopify API tokens available
"""

import sqlite3
import requests
from datetime import datetime, date
import os
import sys

# Configuration
DATABASE_PATH = os.path.expanduser("~/clawd/workstreams/database-setup/society_brands_local.db")
DEFINITE_API_KEY = "acb226c2489e4e5c8ba43c92b5153829-SvrhStC3utT0JSuEgULdLH7bngvQKR9h"
DEFINITE_API_BASE = "https://api.definite.app/v1"

# 11 Society Brands Shopify stores
SHOPIFY_STORES = {
    "activechairs": "AC",
    "clarifion": "CLARIFION",
    "capsule": "CAPSULE",
    "cleanomic": "CLEANOMIC",
    "clubearlybird": "CEB",
    "crunchibeauty": "CRUNCHI",
    "damnnearkiltem": "DNKE",
    "primallifeorganics": "PLO",
    "powertheory": "PT",
    "wolftacticalusa": "WOLF",
    "yankeetoybox": "YTB"
}

def log(message, level="INFO"):
    """Simple logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def query_definite(sql):
    """Query Definite API"""
    headers = {"Authorization": f"Bearer {DEFINITE_API_KEY}"}
    payload = {"sql": sql}
    
    try:
        response = requests.post(f"{DEFINITE_API_BASE}/query", json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        log(f"Definite API error: {e}", "ERROR")
        return []

def extract_inventory_from_definite():
    """
    Extract current inventory from Definite SHOPIFY tables
    
    Strategy:
    - Query SHOPIFY.product_variants directly (has inventory_quantity field)
    - Join with products for product titles
    - Simpler query, less JOIN complexity
    
    Note: Definite may not have real-time inventory (syncs hourly/daily)
    """
    log("Extracting inventory from Definite...")
    
    # Simplified SQL - get inventory directly from product_variants
    sql = """
    SELECT 
        CASE 
            WHEN v.sku LIKE 'AC-%' THEN 'Active Charis'
            WHEN v.sku LIKE 'CLF-%' OR v.sku LIKE 'AS-%' THEN 'Clarifion'
            WHEN v.sku LIKE 'CAPSULE-%' OR v.sku LIKE 'CS-%' THEN 'PureCaps USA'
            WHEN v.sku LIKE 'CLN-%' THEN 'Cleanomic'
            WHEN v.sku LIKE 'CEB-%' THEN 'Club EarlyBird'
            WHEN v.sku LIKE 'CRN-%' OR v.sku LIKE 'CRUNCHI-%' THEN 'Crunchi'
            WHEN v.sku LIKE 'DNKE-%' THEN 'Damn Near Kilt Em'
            WHEN v.sku LIKE 'PLO-%' THEN 'Primal Life Organics'
            WHEN v.sku LIKE 'PT-%' THEN 'Power Theory'
            WHEN v.sku LIKE 'WOLF-%' OR v.sku LIKE 'WT-%' THEN 'Wolf Tactical'
            WHEN v.sku LIKE 'YTB-%' THEN 'Yankee Toybox'
            ELSE 'Unknown'
        END as brand,
        v.sku,
        p.title as product_title,
        v.title as variant_title,
        COALESCE(v.inventory_quantity, 0) as available,
        0 as committed,
        0 as incoming,
        'Default' as location_name
    FROM SHOPIFY.product_variants v
    JOIN SHOPIFY.products p ON v.product_id = p.id
    WHERE v.sku IS NOT NULL
        AND v.sku != ''
        AND v.inventory_quantity > 0
    ORDER BY brand, v.sku
    LIMIT 5000
    """
    
    results = query_definite(sql)
    log(f"Retrieved {len(results)} inventory records from Definite")
    
    return results

def insert_inventory_snapshot(conn, snapshot_date, inventory_records):
    """Insert inventory records into inventory_snapshot table"""
    cursor = conn.cursor()
    
    inserted = 0
    for record in inventory_records:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO inventory_snapshot (
                    snapshot_date, brand, sku, product_title, variant_title,
                    shopify_available, shopify_committed, shopify_incoming, shopify_location
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot_date,
                record.get('brand', 'Unknown'),
                record.get('sku', ''),
                record.get('product_title', ''),
                record.get('variant_title', ''),
                record.get('available', 0),
                record.get('committed', 0),
                record.get('incoming', 0),
                record.get('location_name', 'Default')
            ))
            inserted += 1
        except sqlite3.Error as e:
            log(f"Error inserting SKU {record.get('sku')}: {e}", "ERROR")
    
    conn.commit()
    log(f"Inserted {inserted} inventory snapshot records")
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
    log("Starting Shopify inventory sync...")
    
    try:
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        log(f"Connected to database: {DATABASE_PATH}")
        
        # Extract inventory from Definite
        inventory_records = extract_inventory_from_definite()
        
        if not inventory_records:
            log("No inventory records found", "WARNING")
            log_execution(conn, 'SNAPSHOT', 0, 0, 0, 0, False, "No records from Definite")
            return
        
        # Count unique brands and SKUs
        brands = set(r.get('brand') for r in inventory_records)
        skus = set(r.get('sku') for r in inventory_records)
        
        log(f"Processing {len(brands)} brands, {len(skus)} SKUs")
        
        # Insert snapshot
        today = date.today()
        records_created = insert_inventory_snapshot(conn, today, inventory_records)
        
        # Log execution
        duration = int((datetime.now() - start_time).total_seconds())
        log_execution(conn, 'SNAPSHOT', len(brands), len(skus), records_created, duration, True, None)
        
        log(f"✅ Inventory sync complete in {duration}s")
        
        # Summary stats
        cursor = conn.cursor()
        cursor.execute("""
            SELECT brand, COUNT(*) as sku_count, SUM(shopify_available) as total_units
            FROM inventory_snapshot
            WHERE snapshot_date = ?
            GROUP BY brand
            ORDER BY total_units DESC
        """, (today,))
        
        log("\n📊 Inventory Snapshot Summary:")
        for row in cursor.fetchall():
            log(f"  {row[0]}: {row[1]} SKUs, {row[2]:,} units")
        
        conn.close()
        
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        duration = int((datetime.now() - start_time).total_seconds())
        try:
            log_execution(conn, 'SNAPSHOT', 0, 0, 0, duration, False, str(e))
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
