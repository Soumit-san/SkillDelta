from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from skillrot_app.db.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.api_route("/ping", methods=["GET", "HEAD", "POST"])
def health_ping():
    """
    Lightweight liveness check — no DB call.
    Use this for frontend wake-up polling and uptime monitoring.
    Always responds immediately even if DB is unreachable.
    """
    return {"status": "ok", "service": "SkillDelta Backend"}


@router.get("/")
def health_check(db: Session = Depends(get_db)):
    """
    Full health check — verifies DB connectivity.
    """
    return {
        "status": "UP",
        "database": "Connected",
        "service": "SkillDelta Backend"
    }
