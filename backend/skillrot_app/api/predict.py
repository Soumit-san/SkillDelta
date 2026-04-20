from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from skillrot_app.db.database import get_db
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.services.decay_service import recalculate_skill_decay
from skillrot_app.core.decay_engine import compute_decay_score

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.get("/{skill_id}")
def predict(skill_id: int, days: int = 7, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # 🔹 Step 1 — Get current real health
    current_health = recalculate_skill_decay(skill, db)

    # 🔹 Step 2 — Get last usage
    history = (
        db.query(SkillHistory)
        .filter(SkillHistory.skill_id == skill.id)
        .order_by(SkillHistory.date.desc())
        .first()
    )

    last_used = history.date if history else skill.learned_date

    days_since_now = (date.today() - last_used).days

    # 🔹 Step 3 — Simulate future without practice
    simulated_days = days_since_now + days

    future_health = compute_decay_score(
        days_since_last_record=days,
        days_since_learned=(date.today() - skill.learned_date).days + days,
        usage_frequency=0.0,  # assume no practice in prediction window
        skill_level=skill.level,
        previous_health=current_health,
        sessions_today=0
    )

    # 🔹 Step 4 — Risk classification
    if future_health < 30:
        risk = "High"
    elif future_health < 50:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "skill": skill.name,
        "current_health": current_health,
        "predicted_health_after_days": future_health,
        "days_checked": days,
        "risk_level": risk
    }