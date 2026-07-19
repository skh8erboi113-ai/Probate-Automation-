# 📖 Detailed User Guide

This guide walks you through every part of the **Real Estate Wholesaling & Probate Automation Platform** in detail.

---

## 1. Getting Started

### Prerequisites
- Python 3.11+
- Git
- A web browser

### Installation

```bash
git clone https://github.com/skh8erboi113-ai/Probate-Automation-.git
cd Probate-Automation-
pip install -r requirements.txt
```

---

## 2. Importing Real Leads (Free Public Data)

### Method A: Using the Auto-Filter (Recommended)

1. Go to the Washington County Assessor website
2. Export the latest property CSV
3. Run the filter:

```bash
cd backend
python auto_filter_county_csv.py ~/Downloads/washington_county_export.csv
```

This creates a clean `probate_leads_YYYY-MM-DD.csv` file.

### Method B: Manual Entry from Oregon Courts

```bash
python real_data_ingest.py
```

Choose option 2 and enter leads found at:
https://webportal.courts.oregon.gov/portal/

---

## 3. Running the Platform

### Start the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Open the Dashboard

Simply open `frontend/index.html` in your browser.

You will see two tables:
- **Leads** — Raw scored leads
- **Deals** — Full pipeline tracking

---

## 4. Complete Workflow

### Step 1: Score Leads
Click **Score** on any new lead.

### Step 2: Start Outreach
Click **Start Outreach** → The system sends simulated email/SMS/call.

### Step 3: Create a Deal
After outreach, click **Create Deal** (new button in full version) or use the API.

### Step 4: Generate Contract
Click **Generate Contract** — creates an offer letter in `/backend/contracts/`.

### Step 5: Hand Off to Closer
Click **Ready for Closing** — generates a full deal packet in `/backend/deal_packets/`.

---

## 5. Weekly Routine

Follow `WEEKLY_CHECKLIST.md` every Monday (15 minutes).

---

## 6. File Locations

| Purpose                    | Location                              |
|---------------------------|---------------------------------------|
| Contracts                 | `backend/contracts/`                  |
| Deal Packets              | `backend/deal_packets/`               |
| Database                  | `data/leads.db`                       |
| Filtered Probate CSVs     | Generated in `backend/` folder        |

---

## 7. API Endpoints Reference

| Endpoint                              | Method | Description                          |
|---------------------------------------|--------|--------------------------------------|
| `/leads`                              | GET    | List all leads                       |
| `/score/{lead_id}`                    | POST   | Score a lead                         |
| `/start-outreach/{lead_id}`           | POST   | Trigger outreach                     |
| `/create-deal/{lead_id}`              | POST   | Create deal + follow-up sequence     |
| `/generate-contract/{deal_id}`        | POST   | Generate offer letter                |
| `/ready-for-closing/{deal_id}`        | POST   | Create deal packet for human closer  |
| `/deals`                              | GET    | List all active deals                |

---

## 8. Customization Tips

- Modify `scorer.py` to adjust scoring weights
- Edit `outreach.py` to change message templates
- Update `deal_manager.py` to change follow-up timing

---

**You now have everything needed to run a professional, zero-cost wholesaling operation.**