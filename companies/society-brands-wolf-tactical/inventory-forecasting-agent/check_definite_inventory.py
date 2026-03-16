#!/usr/bin/env python3
"""Quick check of what Shopify inventory data exists in Definite"""

import requests

DEFINITE_API_KEY = "acb226c2489e4e5c8ba43c92b5153829-SvrhStC3utT0JSuEgULdLH7bngvQKR9h"
DEFINITE_API_BASE = "https://api.definite.app/v1"

def query(sql):
    headers = {"Authorization": f"Bearer {DEFINITE_API_KEY}"}
    response = requests.post(f"{DEFINITE_API_BASE}/query", json={"sql": sql}, headers=headers, timeout=120)
    response.raise_for_status()
    return response.json().get("data", [])

# Check inventory_levels table
print("Checking SHOPIFY.inventory_levels...")
try:
    result = query("SELECT COUNT(*) as count FROM SHOPIFY.inventory_levels LIMIT 1")
    print(f"✅ Found {result[0]['count']} records in SHOPIFY.inventory_levels")
except Exception as e:
    print(f"❌ Error: {e}")

# Check inventory_items table
print("\nChecking SHOPIFY.inventory_items...")
try:
    result = query("SELECT COUNT(*) as count FROM SHOPIFY.inventory_items LIMIT 1")
    print(f"✅ Found {result[0]['count']} records in SHOPIFY.inventory_items")
except Exception as e:
    print(f"❌ Error: {e}")

# Check product_variants with inventory
print("\nChecking SHOPIFY.product_variants...")
try:
    result = query("SELECT sku, inventory_quantity FROM SHOPIFY.product_variants WHERE inventory_quantity > 0 LIMIT 5")
    print(f"✅ Sample variants:")
    for r in result:
        print(f"  SKU: {r['sku']}, Qty: {r['inventory_quantity']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Alternative: Check if we have unified products table with inventory
print("\nChecking SHOPIFY.unified_product_variants...")
try:
    result = query("SELECT sku, inventory_quantity FROM SHOPIFY.unified_product_variants WHERE inventory_quantity > 0 LIMIT 5")
    print(f"✅ Sample unified variants:")
    for r in result:
        print(f"  SKU: {r['sku']}, Qty: {r['inventory_quantity']}")
except Exception as e:
    print(f"❌ Error: {e}")
