from datetime import datetime
import json

def trigger_outreach(lead_row):
    """Automated multi-channel outreach (mocked for demo)"""
    lead_id, address, owner_name, _, _, _, _, _, score, _, _, _ = lead_row
    
    channels = ["email", "sms", "call"]
    results = []
    
    for channel in channels:
        if channel == "email":
            msg = f"Hi {owner_name.split()[0]}, interested in your property at {address}. Quick cash offer available."
        elif channel == "sms":
            msg = f"Cash offer for {address}? Reply YES to learn more."
        else:
            msg = f"Automated voice call: 'Hello, this is an automated call regarding your property at {address}. Press 1 to connect to an agent.'"
        
        results.append({
            "channel": channel,
            "message": msg,
            "status": "sent",
            "timestamp": datetime.now().isoformat()
        })
    
    return {
        "lead_id": lead_id,
        "outreach_initiated": True,
        "channels": results,
        "next_step": "Monitor responses. Human will take over at 'ready_for_closing' stage."
    }