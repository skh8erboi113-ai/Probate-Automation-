"""
Deal Manager - Full Backend CRM & Pipeline
Handles deals, follow-ups, responses, and human handoff.
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
import json

DB_PATH = "../data/leads.db"

def init_deal_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Deals table (extends leads)
    c.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        stage TEXT DEFAULT 'new',
        equity REAL,
        motivation_score REAL,
        assigned_closer TEXT,
        contract_generated INTEGER DEFAULT 0,
        last_activity TEXT,
        notes TEXT,
        FOREIGN KEY(lead_id) REFERENCES leads(id)
    )''')
    
    # Follow-up schedule
    c.execute('''CREATE TABLE IF NOT EXISTS follow_ups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER,
        scheduled_date TEXT,
        channel TEXT,
        message TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(deal_id) REFERENCES deals(id)
    )''')
    
    # Responses log
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER,
        channel TEXT,
        received_at TEXT,
        content TEXT,
        sentiment TEXT,
        action_taken TEXT,
        FOREIGN KEY(deal_id) REFERENCES deals(id)
    )''')
    
    conn.commit()
    conn.close()
    print("✅ Deal tables initialized")

def create_deal(lead_id: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create deal record
    c.execute('''INSERT INTO deals (lead_id, stage, last_activity) 
                 VALUES (?, 'new', ?)''', (lead_id, datetime.now().isoformat()))
    deal_id = c.lastrowid
    
    # Create initial follow-up schedule
    schedule_follow_ups(deal_id, conn)
    
    conn.commit()
    conn.close()
    return deal_id

def schedule_follow_ups(deal_id: int, conn=None):
    """Creates automated follow-up sequence"""
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        close_conn = True
    else:
        close_conn = False
    
    c = conn.cursor()
    
    # 7-touch sequence
    schedule = [
        (3, "sms", "Just checking in on your property at {address}. Still interested in a cash offer?"),
        (7, "email", "Quick follow-up: Would you be open to a no-obligation cash offer this week?"),
        (14, "call", "Automated call reminder: Property cash offer available"),
        (21, "sms", "Last chance this month for a fast cash closing on your home."),
        (30, "email", "Final follow-up - let us know if you're still considering selling."),
    ]
    
    for days, channel, message in schedule:
        scheduled = (datetime.now() + timedelta(days=days)).isoformat()
        c.execute('''INSERT INTO follow_ups (deal_id, scheduled_date, channel, message, status)
                     VALUES (?, ?, ?, ?, 'pending')''', 
                  (deal_id, scheduled, channel, message))
    
    if close_conn:
        conn.commit()
        conn.close()

def log_response(deal_id: int, channel: str, content: str, sentiment: str = "neutral"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''INSERT INTO responses (deal_id, channel, received_at, content, sentiment, action_taken)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (deal_id, channel, datetime.now().isoformat(), content, sentiment, "logged"))
    
    # Update deal stage based on response
    if sentiment == "positive":
        c.execute("UPDATE deals SET stage='engaged', last_activity=? WHERE id=?",
                  (datetime.now().isoformat(), deal_id))
    elif sentiment == "interested":
        c.execute("UPDATE deals SET stage='negotiating', last_activity=? WHERE id=?",
                  (datetime.now().isoformat(), deal_id))
    
    conn.commit()
    conn.close()
    return {"status": "response logged", "deal_id": deal_id}

def generate_contract(deal_id: int) -> str:
    """Generates a simple offer letter (text version)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT l.address, l.owner_name, l.estimated_value, d.equity 
                 FROM deals d JOIN leads l ON d.lead_id = l.id WHERE d.id=?''', (deal_id,))
    row = c.fetchone()
    
    if not row:
        return "Deal not found"
    
    address, owner, value, equity = row
    offer_price = int(value * 0.65)  # 65% of ARV as example
    
    contract_text = f"""
CASH OFFER LETTER
Date: {datetime.now().strftime('%B %d, %Y')}

Dear {owner},

We are pleased to present a cash offer for your property located at:

{address}

Our offer: ${offer_price:,}

This is a no-contingency, all-cash offer with a 7-day closing.

Please reply to this message or call us to discuss.

Best regards,
Wholesale Team
"""
    
    # Mark as generated
    c.execute("UPDATE deals SET contract_generated=1, stage='contract_sent' WHERE id=?", (deal_id,))
    conn.commit()
    conn.close()
    
    # Save to file
    filename = f"../backend/contracts/offer_{deal_id}.txt"
    with open(filename, "w") as f:
        f.write(contract_text)
    
    return filename

def mark_ready_for_closing(deal_id: int, closer: str = "Human Closer"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''UPDATE deals SET stage='ready_for_closing', assigned_closer=?, last_activity=?
                 WHERE id=?''', (closer, datetime.now().isoformat(), deal_id))
    
    conn.commit()
    conn.close()
    
    # Create deal packet
    return create_deal_packet(deal_id)

def create_deal_packet(deal_id: int) -> str:
    """Creates a complete handoff packet for the human closer"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT l.*, d.stage, d.equity, d.motivation_score 
                 FROM deals d JOIN leads l ON d.lead_id = l.id WHERE d.id=?''', (deal_id,))
    lead = c.fetchone()
    
    packet = {
        "deal_id": deal_id,
        "lead_data": dict(zip([col[0] for col in c.description], lead)) if lead else {},
        "responses": [],
        "follow_ups_completed": [],
        "recommended_offer": "See contract",
        "next_action": "Human call + present contract"
    }
    
    # Get responses
    c.execute("SELECT * FROM responses WHERE deal_id=?", (deal_id,))
    packet["responses"] = [dict(zip([col[0] for col in c.description], r)) for r in c.fetchall()]
    
    conn.close()
    
    filename = f"../backend/deal_packets/deal_{deal_id}_packet.json"
    with open(filename, "w") as f:
        json.dump(packet, f, indent=2)
    
    return filename

# Initialize tables on import
init_deal_tables()