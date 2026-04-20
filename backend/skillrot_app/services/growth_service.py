from sqlalchemy.orm import Session
from skillrot_app.models.skill_health_history import SkillHealthHistory
from skillrot_app.models.skill import Skill
from sqlalchemy import asc


def get_growth_data(skill_id: int, db: Session):

    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if not skill:
        return None

    history = (
        db.query(SkillHealthHistory)
        .filter(SkillHealthHistory.skill_id == skill_id)
        .order_by(asc(SkillHealthHistory.recorded_at))
        .all()
    )

    if not history:
        return {
            "skill": skill.name,
            "current_health": None,
            "trend": "no_data",
            "history": [],
            "moving_average": None
        }

    history_data = []
    health_values = []

    for entry in history:
        history_data.append({
            "date": entry.recorded_at.strftime("%Y-%m-%d"),
            "health": round(entry.health, 2)
        })
        health_values.append(entry.health)

    current_health = round(health_values[-1], 2)

    # 🔹 TREND CALCULATION
    if len(health_values) >= 2:
        if health_values[-1] > health_values[0]:
            trend = "improving"
        elif health_values[-1] < health_values[0]:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"

    # 🔹 MOVING AVERAGE (Last 5 entries)
    last_n = health_values[-5:]
    moving_avg = round(sum(last_n) / len(last_n), 2)

    return {
        "skill": skill.name,
        "current_health": current_health,
        "trend": trend,
        "history": history_data,
        "moving_average": moving_avg
    }