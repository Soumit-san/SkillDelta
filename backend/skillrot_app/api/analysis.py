from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_health_history import SkillHealthHistory
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.core.skill_analyzer import classify_skill
from skillrot_app.services.decay_service import recalculate_skill_decay
from skillrot_app.core.decay_engine import compute_decay_score
from datetime import date, timedelta

router = APIRouter(prefix="/analysis", tags=["Skill Analysis"])

# -------------------------
# Skill Health API
# -------------------------
@router.get("/skills/{skill_id}/health")
def get_skill_health(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    score = recalculate_skill_decay(skill, db)
    status = classify_skill(score)

    return {
        "skill_id": skill_id,
        "health": score,
        "status": status
    }

# -------------------------
# Decay Curve API
# -------------------------
@router.get("/skills/{skill_id}/decay-curve")
def get_decay_curve(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Ensure today's decay is captured
    current_health = recalculate_skill_decay(skill, db)

    history = (
        db.query(SkillHistory)
        .filter(SkillHistory.skill_id == skill_id)
        .order_by(SkillHistory.date.desc())
        .first()
    )
    last_used = history.date if history else skill.learned_date
    days_since_now = (date.today() - last_used).days
    
    # Generate 14-day future decay projection
    curve = []
    today = date.today()
    level = skill.level.lower() if skill.level else "intermediate"
    
    for i in range(15):
        future_health = compute_decay_score(
            days_since_last_record=i,
            days_since_learned=0,
            usage_frequency=0.0,
            skill_level=level,
            previous_health=current_health,
            sessions_today=0
        )
        curve.append({
            "date": (today + timedelta(days=i)).strftime("%Y-%m-%d"),
            "score": round(future_health, 2)
        })

    return curve

# -------------------------
# Manual Refresh API
# -------------------------
@router.post("/skills/{skill_id}/refresh")
def refresh_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    score = recalculate_skill_decay(skill, db)
    return {
        "message": "Skill refreshed successfully",
        "health": score
    }
