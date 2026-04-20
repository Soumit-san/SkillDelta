from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from skillrot_app.db.database import get_db
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.models.subtopic import Subtopic
from skillrot_app.services.decay_service import recalculate_skill_decay

router = APIRouter(prefix="/practice", tags=["Practice"])


@router.post("/skills/{skill_id}")
def practice_skill(skill_id: int, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Add usage entry
    history = SkillHistory(
        skill_id=skill_id,
        date=date.today(),
        usage=1
    )

    db.add(history)

    # Boost subtopics
    subtopics = db.query(Subtopic).filter(Subtopic.skill_id == skill_id).all()
    for sub in subtopics:
        sub.health_score = min(100, sub.health_score + 10)
        sub.last_practiced = date.today()

    db.commit()

    new_health = recalculate_skill_decay(skill, db)

    return {
        "message": "Practice logged successfully",
        "new_health": new_health
    }