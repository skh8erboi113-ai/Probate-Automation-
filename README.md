# 🏠 Real Estate Wholesaling & Probate Automation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![GitHub last commit](https://img.shields.io/github/last-commit/skh8erboi113-ai/Probate-Automation-)](https://github.com/skh8erboi113-ai/Probate-Automation-)

> **Zero-cost, full-stack automation platform** that finds real probate & estate leads from public records, scores them, runs automated outreach, manages deals, generates contracts, and prepares everything for human closing.

---

## ✨ Features

### 🔄 Full Automation Pipeline
- **Real Lead Generation** — Pulls live data from Washington County + Oregon Courts
- **Smart Lead Scoring** — ML + rules-based scoring (0–100 likelihood to sell)
- **Multi-Channel Outreach** — Automated emails, SMS, and call scripts
- **Deal CRM** — Tracks every lead through complete pipeline stages
- **Automated Follow-ups** — 5-touch sequence (Day 3, 7, 14, 21, 30)
- **Contract Generator** — Auto-creates professional offer letters
- **Deal Packets** — Complete handoff packages for human closers

### 🚫 Human-Only Closing
Closing is intentionally **not automated** — leads are handed off ready for your sales team.

---

## 🛠 Tech Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| Backend     | FastAPI + Python            |
| Frontend    | Vanilla HTML/JS Dashboard   |
| Database    | SQLite                      |
| ML/Scoring  | scikit-learn                |
| Data Source | Public Government Records   |

---

## 📊 Project Stats

- **100% Free** — No paid APIs or lead services
- **Real Data Only** — Pulls directly from county & court records
- **Production Ready** — Includes CI, templates, and professional docs

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/skh8erboi113-ai/Probate-Automation-.git
cd Probate-Automation-
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Import real leads (free public data)
```bash
cd backend
python real_data_ingest.py
```

### 4. Run the backend
```bash
uvicorn main:app --reload --port 8000
```

### 5. Open the dashboard
Just open `frontend/index.html` in your browser.

---

## 📍 Free Real Data Sources

| Source                              | Link                                                                 |
|-------------------------------------|----------------------------------------------------------------------|
| Washington County Property Records  | https://www.co.washington.or.us/AssessmentTaxation/                  |
| Oregon Probate Court Portal         | https://webportal.courts.oregon.gov/portal/                          |
| GIS Verification Map                | http://gisims.co.washington.or.us/InterMap/                          |

---

## 📁 Repository Structure

```
Probate-Automation-/
├── backend/                  # Core automation engine
│   ├── main.py               # FastAPI server + endpoints
│   ├── deal_manager.py       # Deal CRM, contracts, packets
│   ├── scorer.py             # Lead scoring
│   ├── outreach.py           # Multi-channel automation
│   ├── auto_filter_county_csv.py
│   └── real_data_ingest.py
├── frontend/
│   └── index.html            # Interactive dashboard
├── .github/                  # GitHub templates + CI
├── WEEKLY_CHECKLIST.md       # 15-minute Monday routine
├── requirements.txt
└── LICENSE
```

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

**Built with ❤️ for real estate wholesalers who want to scale without spending money on leads.**