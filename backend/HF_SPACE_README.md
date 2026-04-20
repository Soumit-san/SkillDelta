---
title: SkillDelta Backend
emoji: 🎯
colorFrom: red
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# SkillDelta Backend API

FastAPI backend for **SkillDelta** — a full-stack skill-tracking application.

## 📡 Endpoints

| Route | Description |
|---|---|
| `GET /` | App info and database status |
| `GET /health/ping` | Lightweight liveness check (no DB) |
| `GET /health/` | Full health check with DB connectivity |
| `GET /docs` | Interactive Swagger UI |
| `GET /redoc` | ReDoc API documentation |

## 🔧 Tech Stack

- **Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL via SQLAlchemy (Supabase)
- **AI:** Groq API
- **OCR:** Tesseract + PDFPlumber
- **Scheduler:** APScheduler

## 🔑 Required Secrets (set in HF Space Settings → Repository Secrets)

```
DATABASE_URL
JWT_SECRET
JWT_ALGORITHM
GROQ_API_KEY
YOUTUBE_API_KEY
EMAIL_ADDRESS
EMAIL_PASSWORD
SENDGRID_API_KEY
CRON_SECRET
APP_NAME
LLM_ENABLED
```

> ⚠️ Never commit your `.env` file. Add all secrets via the HF Space Settings UI.
