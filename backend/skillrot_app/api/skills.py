from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.models.skill import Skill
from skillrot_app.schemas.skill import SkillCreate, SkillOut
from skillrot_app.core.security import get_current_user
from skillrot_app.models.user import User

# 🔥 Import dependent models for explicit cascade deletion
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.models.assessment import Assessment
from skillrot_app.models.reminder import Reminder
from skillrot_app.models.skill_health_history import SkillHealthHistory
from skillrot_app.models.subtopic import Subtopic

router = APIRouter(prefix="/skills", tags=["Skills"])


# ✅ CREATE SKILL (JWT Protected)
@router.post("/", response_model=SkillOut)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_skill = Skill(
        name=skill.name,
        level=skill.level,
        learned_date=skill.learned_date,
        user_id=current_user.id  # 🔥 auto attach logged-in user
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


# ✅ GET SKILL BY ID (Only Owner Can Read)
@router.get("/{skill_id:int}", response_model=SkillOut)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = (
        db.query(Skill)
        .filter(
            Skill.id == skill_id,
            Skill.user_id == current_user.id  # 🔥 owner check
        )
        .first()
    )

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return skill


# ✅ UPDATE SKILL (Only Owner Can Update)
@router.put("/{skill_id:int}", response_model=SkillOut)
def update_skill(
    skill_id: int,
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_skill = (
        db.query(Skill)
        .filter(
            Skill.id == skill_id,
            Skill.user_id == current_user.id  # 🔥 owner check
        )
        .first()
    )

    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db_skill.name = skill.name
    db_skill.level = skill.level
    db_skill.learned_date = skill.learned_date

    db.commit()
    db.refresh(db_skill)

    return db_skill


# ✅ DELETE SKILL (Only Owner Can Delete)
@router.delete("/{skill_id:int}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = (
        db.query(Skill)
        .filter(
            Skill.id == skill_id,
            Skill.user_id == current_user.id  # 🔥 owner check
        )
        .first()
    )

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # 🔥 Manually delete dependent records to avoid IntegrityError (if relationships lack cascade="all,delete")
    db.query(SkillHistory).filter(SkillHistory.skill_id == skill_id).delete(synchronize_session=False)
    db.query(Assessment).filter(Assessment.skill_id == skill_id).delete(synchronize_session=False)
    db.query(Reminder).filter(Reminder.skill_id == skill_id).delete(synchronize_session=False)
    db.query(SkillHealthHistory).filter(SkillHealthHistory.skill_id == skill_id).delete(synchronize_session=False)
    db.query(Subtopic).filter(Subtopic.skill_id == skill_id).delete(synchronize_session=False)

    db.delete(skill)
    db.commit()

    return {"message": "Skill deleted successfully"}
