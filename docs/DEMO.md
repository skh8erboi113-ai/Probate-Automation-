# 🎥 Demo Guide

This document explains how to run a full end-to-end demo of the platform.

---

## Demo Goals

Show the complete flow:
1. Import real probate leads
2. Score leads
3. Run automated outreach
4. Create deal + follow-ups
5. Generate contract
6. Create deal packet for human closer

---

## Step-by-Step Demo (10–15 minutes)

### 1. Prepare Sample Data

```bash
cd backend
python real_data_ingest.py
```

Use **Option 2** and enter 3–5 realistic probate leads.

### 2. Start the Backend

```bash
uvicorn main:app --reload --port 8000
```

### 3. Open Dashboard

Open `frontend/index.html`

### 4. Walk Through the Flow

| Action                    | Button to Click              | Expected Result                              |
|---------------------------|------------------------------|----------------------------------------------|
| Score leads               | **Score**                    | Score appears (e.g. 82)                      |
| Start outreach            | **Start Outreach**           | Alert shows email/SMS/call sent              |
| Create deal               | Use API or extend dashboard  | Deal created with 5 follow-ups scheduled     |
| Generate contract         | **Generate Contract**        | Offer letter saved in `backend/contracts/`   |
| Ready for closing         | **Ready for Closing**        | Deal packet created in `backend/deal_packets/` |

---

## Sample Demo Script (for video or live demo)

> "Good morning. Today I'm going to show you how we automate the entire front end of real estate wholesaling using only free public records."

1. Show the county website and how we pull leads
2. Run the auto-filter script
3. Open dashboard and score 3 leads
4. Trigger outreach and show the messages
5. Create a deal and show the follow-up schedule
6. Generate a contract
7. Create the final deal packet and explain handoff to closer

---

## Demo Assets You Can Create

- Record a 2–3 minute Loom or YouTube video
- Take screenshots of the dashboard at each stage
- Add a `demo/` folder with sample screenshots

---

## Tips for a Great Demo

- Use realistic lead names and addresses
- Show the generated files in the file explorer
- Emphasize that everything is 100% free

---

**You now have everything needed to create a compelling demo of the platform.**