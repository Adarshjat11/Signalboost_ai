# SignalBoost AI

**Smart Lead Generation Platform** for Caprae Capital – built with Python (FastAPI), React (Tailwind), and data from Crunchbase, LinkedIn, and job boards.

---

## 🚀 Overview

SignalBoost AI is a full-stack lead generation tool that identifies and ranks high-potential B2B leads based on real-time data from public sources. It enriches them using custom scoring logic and email verification, and displays them in a responsive frontend dashboard.

---

## 🧠 Key Features

- 🔍 Scraping from LinkedIn, Crunchbase, and job boards
- 🎯 Rule-based lead scoring (title, keywords, funding, etc.)
- 📧 Email verification with Hunter API
- 📊 React + Tailwind UI for filtering, sorting, exporting
- 📈 Streamlit dashboard for visual insights
- ⚡ FastAPI backend with `/generate-leads` endpoint

---

## 🖼️ Architecture

```
Frontend (React + Tailwind)
       |
    FastAPI (main.py)
       |
Scrapers + Scorers (LinkedIn, Crunchbase, Job Boards)
       |
 Hunter API + Rule Engine
       |
     CSV Export + Dashboard (Streamlit)
```

---

## 🛠 Setup Instructions

### ✅ 1. Backend

```bash
cd signalboost_full_project
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: http://localhost:8000

> Make sure `.env` includes your Hunter API key.

---

### ✅ 2. Frontend

```bash
cd signalboost_fresh_react_tailwind_app
npm install
npm start
```

Visit: http://localhost:3000

---

### ✅ 3. Dashboard

```bash
cd signalboost_full_project
streamlit run dashboard.py
```

Visit: http://localhost:8501

---

## 📁 Folder Structure

```
├── main.py               # FastAPI backend
├── hunter.py             # Email verification logic
├── rule_based.py         # Lead scoring logic
├── linkedin_scraper.py
├── crunchbase_scraper.py
├── job_board_scraper.py
├── dashboard.py          # Streamlit visual analytics
├── enriched_leads.csv    # Output lead file
├── requirements.txt
├── README.md             # Setup guide
├── frontend/             # React + Tailwind UI
```

---

## ✨ Example

![example UI](https://dummyimage.com/1200x400/ddd/000&text=SignalBoost+Lead+UI)

---

## 📫 Contact

Adarsh Jat
Built with ❤️ for Caprae Capital.
