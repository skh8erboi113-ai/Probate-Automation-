"""
FREE Real Data Ingestion for Washington County, OR + Oregon Probate
No paid APIs. Uses only public records.

Sources (all free):
1. Washington County Property Search → https://www.co.washington.or.us/AssessmentTaxation/
2. Oregon Courts Probate Portal → https://webportal.courts.oregon.gov/portal/
3. GIS Map: http://gisims.co.washington.or.us/InterMap/
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

DB_PATH = "../data/leads.db"

def import_from_county_csv(csv_path):
    """
    Import estate/probate leads from Washington County public CSV export.
    
    How to get the file (FREE):
    1. Go to: https://www.co.washington.or.us/AssessmentTaxation/
    2. Use their Property Search or request bulk data
    3. Filter for "owner name contains ESTATE, DECEASED, or TRUST"
    4. Export as CSV and save locally
    """
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return 0
    
    df = pd.read_csv(csv_path)
    
    # Standardize columns (adjust based on county export format)
    required = ['address', 'owner_name', 'estimated_value', 'owner_age']
    if not all(col in df.columns for col in required):
        print("CSV missing required columns. Rename columns to: address, owner_name, estimated_value, owner_age, days_on_market, probate_status")
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    
    count = 0
    for _, row in df.iterrows():
        try:
            conn.execute('''
                INSERT OR IGNORE INTO leads 
                (address, owner_name, property_type, estimated_value, owner_age, 
                 days_on_market, probate_status, score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('address'),
                row.get('owner_name'),
                row.get('property_type', 'Single Family'),
                float(row.get('estimated_value', 0)),
                int(row.get('owner_age', 65)),
                int(row.get('days_on_market', 90)),
                row.get('probate_status', 'yes'),
                None,
                'new'
            ))
            count += 1
        except Exception as e:
            continue
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {count} real probate/estate leads from county data")
    return count

def manual_probate_entry():
    """Simple CLI tool for entering leads found from Oregon Courts portal"""
    print("\n=== Manual Entry from Oregon Court Records ===")
    print("1. Visit: https://webportal.courts.oregon.gov/portal/")
    print("2. Search probate cases in Washington County")
    print("3. Enter the details below:\n")
    
    address = input("Property Address: ")
    owner = input("Owner / Estate Name: ")
    value = float(input("Est. Value (from assessor): "))
    age = int(input("Owner Age (approx): "))
    dom = int(input("Days on Market (or 120): "))
    probate = input("Probate Status (yes/pending): ")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO leads 
        (address, owner_name, property_type, estimated_value, owner_age, 
         days_on_market, probate_status, score, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (address, owner, 'Single Family', value, age, dom, probate, None, 'new'))
    conn.commit()
    conn.close()
    print("✅ Real lead added from public records!")

if __name__ == "__main__":
    print("Real Data Ingestion Tool (FREE)")
    print("1. Import from Washington County CSV")
    print("2. Manual entry from Oregon Probate Portal")
    
    choice = input("Choice (1 or 2): ")
    if choice == "1":
        path = input("Path to your county CSV file: ")
        import_from_county_csv(path)
    else:
        manual_probate_entry()