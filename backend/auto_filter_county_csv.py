"""
Auto-Filter for Washington County Property CSV Exports
Filters for probate/estate leads automatically.
"""

import pandas as pd
import os
import sys
from datetime import datetime

PROBATE_KEYWORDS = [
    'estate', 'deceased', 'trust', 'heirs', 'executor', 
    'est of', 'estate of', 'decd', 'dec\'d', 'probate'
]

def filter_probate_leads(input_csv, output_csv=None):
    if not os.path.exists(input_csv):
        print(f"❌ File not found: {input_csv}")
        return None
    
    print(f"📥 Reading {input_csv}...")
    df = pd.read_csv(input_csv)
    
    # Try to find the owner column (common variations)
    owner_col = None
    for col in df.columns:
        if any(x in col.lower() for x in ['owner', 'name', 'taxpayer']):
            owner_col = col
            break
    
    if not owner_col:
        print("❌ Could not find owner name column. Columns available:", list(df.columns))
        return None
    
    print(f"🔍 Filtering on column: {owner_col}")
    
    # Create a mask for probate keywords
    mask = df[owner_col].astype(str).str.lower().str.contains(
        '|'.join(PROBATE_KEYWORDS), na=False, regex=True
    )
    
    probate_df = df[mask].copy()
    
    if len(probate_df) == 0:
        print("⚠️ No probate/estate leads found in this file.")
        return None
    
    # Standardize columns for our system
    probate_df = probate_df.rename(columns={
        owner_col: 'owner_name',
        'SitusAddress': 'address',
        'TotalMarketValue': 'estimated_value',
        'OwnerAge': 'owner_age'
    })
    
    # Add missing columns
    probate_df['property_type'] = 'Single Family'
    probate_df['days_on_market'] = 120
    probate_df['probate_status'] = 'yes'
    
    # Keep only columns we need
    cols_to_keep = ['address', 'owner_name', 'property_type', 
                    'estimated_value', 'owner_age', 'days_on_market', 'probate_status']
    probate_df = probate_df[[c for c in cols_to_keep if c in probate_df.columns]]
    
    if output_csv is None:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_csv = f"probate_leads_{timestamp}.csv"
    
    probate_df.to_csv(output_csv, index=False)
    print(f"✅ Found {len(probate_df)} probate/estate leads!")
    print(f"💾 Saved to: {output_csv}")
    
    return output_csv

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_filter_county_csv.py path/to/county_export.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    filter_probate_leads(input_file)