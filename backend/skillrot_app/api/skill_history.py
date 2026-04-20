from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.schemas.skill_history import SkillUsageCreate

router = APIRouter(prefix="/skills", tags=["Skill History"])

@router.post("/{skill_id}/usage")
def log_skill_usage(
    skill_id: int,
    usage: SkillUsageCreate,
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    history = SkillHistory(
        skill_id=skill_id,
        date=usage.date,
        usage=usage.usage,
        decay_score=None
    )

    db.add(history)
    db.commit()

    return {"message": "Usage logged successfully"}
