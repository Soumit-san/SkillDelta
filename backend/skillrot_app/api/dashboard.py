from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from skillrot_app.db.database import get_db
from skillrot_app.models.user import User
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.models.reminder import Reminder
from skillrot_app.models.skill_health_history import SkillHealthHistory
from skillrot_app.services.decay_service import recalculate_skill_decay
from skillrot_app.core.skill_analyzer import classify_skill
from skillrot_app.core.decay_engine import compute_decay_score

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/user/{user_id}")
def get_user_dashboard(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    skills = db.query(Skill).filter(Skill.user_id == user_id).all()
    
    if not skills:
        return []

    skill_ids = [s.id for s in skills]

    # 1. Bulk fetch latest health (since recalculate_skill_decay on GET is too slow)
    # We rely on the health calculated from the daily cron job or explicit practice actions
    health_records = (
        db.query(SkillHealthHistory)
        .filter(SkillHealthHistory.skill_id.in_(skill_ids))
        .order_by(SkillHealthHistory.skill_id, SkillHealthHistory.recorded_at.desc())
        .all()
    )
    
    # 2. Bulk fetch practice history
    practice_history = (
        db.query(SkillHistory)
        .filter(SkillHistory.skill_id.in_(skill_ids))
        .order_by(SkillHistory.skill_id, SkillHistory.date.desc())
        .all()
    )
    
    # 3. Bulk fetch reminder counts
    from sqlalchemy import func
    reminders = (
        db.query(Reminder.skill_id, func.count(Reminder.id).label("count"))
        .filter(Reminder.skill_id.in_(skill_ids))
        .group_by(Reminder.skill_id)
        .all()
    )
    reminder_counts = {r.skill_id: r.count for r in reminders}

    # Process grouped records
    health_map = {}
    for h in health_records:
        if h.skill_id not in health_map:
            health_map[h.skill_id] = []
        health_map[h.skill_id].append(h)

    history_map = {}
    for ph in practice_history:
        if ph.skill_id not in history_map:
            history_map[ph.skill_id] = []
        history_map[ph.skill_id].append(ph)

    result = []
    
    today = date.today()

    for skill in skills:
        # Get health
        s_health_records = health_map.get(skill.id, [])
        if s_health_records:
            health = s_health_records[0].health
            days_since = (today - s_health_records[0].recorded_at.date()).days
            # Approximate current health if it hasn't been updated today (fallback)
            if days_since > 0:
                 health = max(0, health - (days_since * 0.5)) 
        else:
            # No health history yet — compute actual decay from learned_date
            # so newly added skills show real health instead of 100%
            days_since_learned = (today - skill.learned_date).days
            level = skill.level.lower() if skill.level else "beginner"
            health = compute_decay_score(
                days_since_last_record=0,
                days_since_learned=days_since_learned,
                usage_frequency=0,
                skill_level=level,
                previous_health=None,
                sessions_today=0
            )
            
        health = round(health, 2)
        status = classify_skill(health)

        # Last practiced
        s_history = history_map.get(skill.id, [])
        last_practiced = s_history[0].date if s_history else skill.learned_date

        # Trend (compare latest two health records)
        trend = "stable"
        if len(s_health_records) >= 2:
            if s_health_records[0].health > s_health_records[1].health:
                trend = "up"
            elif s_health_records[0].health < s_health_records[1].health:
                trend = "down"

        # Reminders
        r_count = reminder_counts.get(skill.id, 0)

        result.append({
            "skill_id": skill.id,
            "skill": skill.name,
            "level": skill.level,
            "health": health,
            "status": status,
            "trend": trend,
            "last_practiced": last_practiced,
            "learned_date": skill.learned_date,
            "reminders": r_count
        })

    return result