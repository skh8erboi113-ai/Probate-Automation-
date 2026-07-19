from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import pandas as pd
from datetime import datetime
import json
from scorer import score_lead
from outreach import trigger_outreach
from deal_manager import (
    create_deal, log_response, generate_contract, 
    mark_ready_for_closing, create_deal_packet
)

app = FastAPI(title="Real Estate Wholesale Automation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "../data/leads.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        owner_name TEXT,
        property_type TEXT,
        estimated_value REAL,
        owner_age INTEGER,
        days_on_market INTEGER,
        probate_status TEXT,
        score REAL,
        status TEXT DEFAULT 'new',
        last_contacted TEXT,
        notes TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

class Lead(BaseModel):
    address: str
    owner_name: str
    property_type: str
    estimated_value: float
    owner_age: int
    days_on_market: int
    probate_status: str

@app.get("/")
def root():
    return {"message": "Real Estate Automation API running"}

@app.post("/generate-leads")
def generate_leads(batch_size: int = 10):
    import subprocess
    result = subprocess.run(["python", "lead_generator.py", str(batch_size)], capture_output=True, text=True, cwd=".")
    return {"status": "success", "generated": batch_size, "output": result.stdout}

@app.get("/leads")
def get_leads():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM leads ORDER BY score DESC", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.post("/score/{lead_id}")
def score_lead_endpoint(lead_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE id=?", (lead_id,))
    row = c.fetchone()
    if not row:
        raise HTTPException(404, "Lead not found")
    
    # Score using ML / rules
    score = score_lead(row)
    
    c.execute("UPDATE leads SET score=?, status='scored' WHERE id=?", (score, lead_id))
    conn.commit()
    conn.close()
    return {"lead_id": lead_id, "score": score}

@app.post("/start-outreach/{lead_id}")
def start_outreach(lead_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE id=?", (lead_id,))
    row = c.fetchone()
    if not row:
        raise HTTPException(404, "Lead not found")
    
    outreach_result = trigger_outreach(row)
    
    c.execute("UPDATE leads SET status='outreach_started', last_contacted=? WHERE id=?", 
              (datetime.now().isoformat(), lead_id))
    conn.commit()
    conn.close()
    
    return outreach_result

@app.post("/mark-ready/{lead_id}")
def mark_ready(lead_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE leads SET status='ready_for_closing' WHERE id=?", (lead_id,))
    conn.commit()
    conn.close()
    return {"message": "Lead marked ready for human closing"}

# ==================== NEW BACKEND ENDPOINTS ====================

@app.post("/create-deal/{lead_id}")
def create_deal_endpoint(lead_id: int):
    deal_id = create_deal(lead_id)
    return {"deal_id": deal_id, "message": "Deal created with follow-up sequence"}

@app.post("/log-response/{deal_id}")
def log_response_endpoint(deal_id: int, channel: str, content: str, sentiment: str = "neutral"):
    result = log_response(deal_id, channel, content, sentiment)
    return result

@app.post("/generate-contract/{deal_id}")
def generate_contract_endpoint(deal_id: int):
    filename = generate_contract(deal_id)
    return {"contract_file": filename, "message": "Offer letter generated"}

@app.post("/ready-for-closing/{deal_id}")
def ready_for_closing_endpoint(deal_id: int):
    packet_file = mark_ready_for_closing(deal_id)
    return {
        "message": "Deal ready for human closing",
        "deal_packet": packet_file
    }

@app.get("/deals")
def get_deals():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT d.*, l.address, l.owner_name, l.score 
        FROM deals d 
        JOIN leads l ON d.lead_id = l.id 
        ORDER BY d.last_activity DESC
    """, conn)
    conn.close()
    return df.to_dict(orient="records")