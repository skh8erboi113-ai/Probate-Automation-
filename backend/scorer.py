import numpy as np

def score_lead(lead_row):
    """
    Rule + ML hybrid scoring for likelihood to sell (0-100)
    Features: owner_age, estimated_value, days_on_market, probate_status
    """
    # Extract fields
    _, address, owner_name, prop_type, est_value, owner_age, dom, probate, score, status, last, notes = lead_row
    
    score_val = 0
    
    # Probate homes get high priority
    if probate.lower() == "yes":
        score_val += 45
    elif probate.lower() == "pending":
        score_val += 30
    
    # High days on market = motivated
    if dom > 120:
        score_val += 25
    elif dom > 60:
        score_val += 15
    
    # Older owners = higher likelihood
    if owner_age > 70:
        score_val += 20
    elif owner_age > 55:
        score_val += 10
    
    # Value range (mid-tier homes easier to wholesale)
    if 150000 < est_value < 450000:
        score_val += 10
    
    # Cap at 100
    final_score = min(max(score_val, 10), 100)
    return round(final_score, 1)