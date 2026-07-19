# 🗓️ Weekly Probate Lead Pipeline Checklist
**Zero-cost • Washington County, OR + Oregon Courts**

## Every Monday (15–20 mins)

### 1. Pull Fresh Probate Data
- [ ] Go to Oregon Courts Portal → https://webportal.courts.oregon.gov/portal/
- [ ] Search: **Washington County** + Case Type = **Probate**
- [ ] Download or screenshot new cases from the past 7 days
- [ ] Use `real_data_ingest.py` → Option 2 (manual entry) for new leads

### 2. Refresh County Property Records
- [ ] Visit Washington County Assessor: https://www.co.washington.or.us/AssessmentTaxation/
- [ ] Export latest property CSV (or request bulk data)
- [ ] Run auto-filter:
  ```bash
  cd backend
  python auto_filter_county_csv.py ~/Downloads/washington_county_export.csv
  ```
- [ ] Import the generated `probate_leads_YYYY-MM-DD.csv` into the system

### 3. Score & Launch Outreach
- [ ] Open dashboard (`frontend/index.html`)
- [ ] Click **Score** on all new leads
- [ ] Click **Start Outreach** on high-scoring leads (70+)

### 4. Review & Clean Up
- [ ] Check status of leads from last week
- [ ] Mark any that have responded as `ready_for_closing`
- [ ] Delete duplicate or low-quality leads

---

## Quick Reference Links

| Task                        | Link                                                                 |
|----------------------------|----------------------------------------------------------------------|
| Oregon Probate Search      | https://webportal.courts.oregon.gov/portal/                          |
| Washington County Assessor | https://www.co.washington.or.us/AssessmentTaxation/                  |
| GIS Map (verify addresses) | http://gisims.co.washington.or.us/InterMap/                          |
| Auto-Filter Script         | `backend/auto_filter_county_csv.py`                                  |

---

**Pro Tip**: Do this every Monday morning. You’ll have a steady stream of fresh, free probate leads every week with almost zero cost.

Print this page or save it as your weekly routine!