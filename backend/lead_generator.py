import sqlite3
import random
import sys
from datetime import datetime

DB_PATH = "../data/leads.db"

def generate_mock_leads(n=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    addresses = [
        "123 Maple St, Portland, OR", "456 Oak Ave, Hillsboro, OR",
        "789 Pine Rd, Beaverton, OR", "101 Cedar Ln, Tigard, OR"
    ]
    names = ["John Smith", "Mary Johnson", "Robert Williams", "Patricia Brown"]
    property_types = ["Single Family", "Multi-Family", "Condo"]
    probate_options = ["yes", "pending", "no"]
    
    for _ in range(n):
        c.execute('''INSERT INTO leads 
        (address, owner_name, property_type, estimated_value, owner_age, days_on_market, probate_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)''', (
            random.choice(addresses),
            random.choice(names),
            random.choice(property_types),
            round(random.uniform(180000, 650000), 0),
            random.randint(45, 85),
            random.randint(30, 300),
            random.choice(probate_options)
        ))
    
    conn.commit()
    conn.close()
    print(f"Generated {n} leads")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    generate_mock_leads(count)