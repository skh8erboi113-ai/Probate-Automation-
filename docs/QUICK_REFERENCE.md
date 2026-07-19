# ⚡ Quick Reference Card

### Most Used Commands

```bash
# Install everything
pip install -r requirements.txt

# Import real leads
cd backend && python real_data_ingest.py

# Start the API
uvicorn main:app --reload --port 8000

# Auto-filter county CSV
python auto_filter_county_csv.py ~/Downloads/county_export.csv
```

### Key Files

| File                          | Purpose                              |
|-------------------------------|--------------------------------------|
| `backend/main.py`             | API server                           |
| `backend/deal_manager.py`     | Deal CRM + contracts                 |
| `backend/scorer.py`           | Lead scoring logic                   |
| `frontend/index.html`         | Dashboard                            |
| `WEEKLY_CHECKLIST.md`         | Monday routine                       |

### Important Folders

- `backend/contracts/` — Generated offer letters
- `backend/deal_packets/` — Handoff packages for closers
- `data/leads.db` — Main database

---

**Keep this card handy for daily use.**