from fastapi import FastAPI
from contextlib import asynccontextmanager
from skillrot_app.core.config import settings
from skillrot_app.core.logging import setup_logging
from skillrot_app.core.exceptions import global_exception_handler
from skillrot_app.core.scheduler import start_scheduler
from skillrot_app.core.keep_alive import self_ping_loop

import asyncio
import logging

# 🔹 Import routers in desired logical order

from skillrot_app.api.auth import router as auth_router
from skillrot_app.api.skills import router as skills_router
from skillrot_app.api.analysis import router as analysis_router
from skillrot_app.api.recommendations import router as recommendations_router
from skillrot_app.api.growth import router as growth_router
from skillrot_app.api.predict import router as predict_router
from skillrot_app.api.assessment import router as assessment_router
from skillrot_app.api.practice import router as practice_router
from skillrot_app.api.dashboard import router as dashboard_router
from skillrot_app.api.reminders import router as reminders_router
from skillrot_app.api.skill_history import router as skill_history_router
from skillrot_app.api.users import router as users_router
from skillrot_app.api.health import router as health_router
from skillrot_app.api.role_filter import router as role_filter_router

# 🔹 DB imports
from skillrot_app.db.database import check_db_connection, engine
from skillrot_app.models.base import Base

# 🔹 Import models for metadata registration
import skillrot_app.models.user
import skillrot_app.models.skill
import skillrot_app.models.skill_history
import skillrot_app.models.subtopic
import skillrot_app.models.skill_health_history
import skillrot_app.models.reminder

import os
from dotenv import load_dotenv

load_dotenv()

print("EMAIL LOADED:", os.getenv("EMAIL_ADDRESS"))

# 🔹 Setup logging FIRST
setup_logging()
logger = logging.getLogger(__name__)

# =========================================================
# 🔹 LIFESPAN (startup + shutdown + keep-alive)
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────
    logger.info("SkillDelta backend starting up...")
    check_db_connection()
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured.")
    start_scheduler()

    # Launch self-ping keep-alive as background task
    ping_task = asyncio.create_task(self_ping_loop())

    yield  # ← app is running

    # ── Shutdown ─────────────────────────────────────────
    ping_task.cancel()
    logger.info("SkillDelta backend shutting down...")


# ✅ Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://skilldelta.netlify.app",
        "https://skilldelta.vercel.app",
        # ✅ Hugging Face Spaces
        "https://samd444-skilldelta.hf.space",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)

# =========================================================
# 🔥 ROUTER ORDER (STRICTLY AS REQUESTED)
# =========================================================

app.include_router(auth_router)            # 1️⃣ Auth
app.include_router(skills_router)          # 2️⃣ Skills
app.include_router(analysis_router)        # 3️⃣ Skill Analysis
app.include_router(recommendations_router) # 4️⃣ Recommendation
app.include_router(growth_router)          # 5️⃣ Growth Analytics
app.include_router(predict_router)         # 6️⃣ Prediction
app.include_router(assessment_router)      # 7️⃣ Assessment
app.include_router(practice_router)        # 8️⃣ Practice
app.include_router(dashboard_router)       # 9️⃣ Dashboard
app.include_router(reminders_router)       # 🔟 Reminder
app.include_router(skill_history_router)   # 11️⃣ Skill History
app.include_router(users_router)           # 12️⃣ User
app.include_router(health_router)          # 13️⃣ Health
app.include_router(role_filter_router)

# =========================================================
# 🔹 STARTUP / SHUTDOWN — handled by lifespan() above
# =========================================================


# =========================================================
# 🔹 DEFAULT ROOT ENDPOINT (LAST)
# =========================================================

@app.get("/")
def root():
    db_url = settings.DATABASE_URL or ""
    if "supabase" in db_url:
        db_type = "Supabase PostgreSQL"
    elif "localhost" in db_url or "127.0.0.1" in db_url:
        db_type = "Local PostgreSQL"
    elif db_url:
        db_type = "Cloud PostgreSQL"
    else:
        db_type = "Unknown DB"

    return {
        "message": "SkillDelta backend running",
        "platform": "Hugging Face Spaces",
        "database": db_type
    }
