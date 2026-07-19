# Real Estate Wholesaling & Probate Automation Platform

## Overview
Full-stack automation platform for wholesaling real estate and probate homes.

**Automated Features:**
- Lead generation (now supports **real public data**)
- Lead scoring (likelihood to sell)
- Automated multi-channel outreach (email, SMS, calls via mocks)
- Response handling & conversation simulation
- Human-only closing (no automation)

**Tech Stack:**
- Backend: Python + FastAPI
- Frontend: Vanilla HTML/JS Dashboard
- Data: SQLite + CSV
- ML: scikit-learn for scoring

## Full Backend Now Integrated ✅

The system now includes a complete backend:

- **Deal CRM** — Every lead becomes a tracked deal with stages
- **Automated Follow-ups** — 5-touch sequence (Day 3, 7, 14, 21, 30)
- **Response Logging** — Log seller replies and auto-update deal stage
- **Contract Generator** — Creates offer letters automatically
- **Deal Packets** — Full handoff package for human closers

## FREE Real Data Sources (No Money Needed)

### 1. Washington County Property Records (Your Location)
- https://www.co.washington.or.us/AssessmentTaxation/
- Search for owners containing: ESTATE, DECEASED, TRUST
- Export CSV or use public terminals

### 2. Oregon Probate Court Records
- https://webportal.courts.oregon.gov/portal/
- Free public search for probate cases
- Use county filter: Washington County

### 3. GIS Map (for verification)
- http://gisims.co.washington.or.us/InterMap/

## Setup & Run

1. Install dependencies:
```bash
pip install fastapi uvicorn pandas scikit-learn sqlalchemy python-multipart
```

2. Import real leads:
```bash
cd backend
python real_data_ingest.py
```

3. Start the backend:
```bash
uvicorn main:app --reload --port 8000
```

4. Open dashboard:
Open `frontend/index.html` in browser.

**Everything runs on public records — 100% free.**