from datetime import date
from sqlalchemy.orm import Session
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_health_history import SkillHealthHistory
from skillrot_app.models.subtopic import Subtopic
from skillrot_app.core.decay_engine import compute_decay_score


def recalculate_skill_decay(skill: Skill, db: Session):

    today = date.today()

    # -----------------------------------------------------
    # 1️⃣ Get Practice History
    # -----------------------------------------------------
    history = (
        db.query(SkillHistory)
        .filter(SkillHistory.skill_id == skill.id)
        .order_by(SkillHistory.date)
        .all()
    )

    if not history:
        usage_freq = 0
        sessions_today = 0
    else:
        used_dates = [h.date for h in history if h.usage == 1]
        
        if used_dates:
            last_used = max(used_dates)
        else:
            last_used = skill.learned_date

        total_sessions = len(history)
        usage_count = len(used_dates)
        usage_freq = usage_count / max(total_sessions, 1)
        sessions_today = len([h for h in history if h.date == today and h.usage == 1])

    # -----------------------------------------------------
    # 2️⃣ Get Previous Health Anchor
    # -----------------------------------------------------
    latest_health_entry = (
        db.query(SkillHealthHistory)
        .filter(SkillHealthHistory.skill_id == skill.id)
        # BUGFIX: We MUST anchor to a day BEFORE today to avoid compounding!
        .filter(SkillHealthHistory.recorded_at < today) 
        .order_by(SkillHealthHistory.recorded_at.desc())
        .first()
    )

    previous_health = (
        latest_health_entry.health if latest_health_entry else None
    )

    if latest_health_entry:
        days_since_last_record = (today - latest_health_entry.recorded_at.date()).days
    else:
        days_since_last_record = 0
        
    days_since_learned = (today - skill.learned_date).days

    # -----------------------------------------------------
    # 3️⃣ Clean Level
    # -----------------------------------------------------
    level = skill.level.lower() if skill.level else "intermediate"

    # -----------------------------------------------------
    # 4️⃣ Compute New Score
    # -----------------------------------------------------
    score = compute_decay_score(
        days_since_last_record=days_since_last_record,
        days_since_learned=days_since_learned,
        usage_frequency=usage_freq,
        skill_level=level,
        previous_health=previous_health,
        sessions_today=sessions_today
    )

    # -----------------------------------------------------
    # 6️⃣ Avoid duplicate same-day entry (Idempotent Upsert)
    # -----------------------------------------------------
    today_health_entry = (
        db.query(SkillHealthHistory)
        .filter(SkillHealthHistory.skill_id == skill.id)
        .filter(SkillHealthHistory.recorded_at >= today)
        .first()
    )

    if today_health_entry:
        # BUGFIX: Don't append infinite rows! Just update today's score if it calculated a new one.
        today_health_entry.health = score
    else:
        db.add(SkillHealthHistory(
            skill_id=skill.id,
            health=score,
            recorded_at=today
        ))

    # -----------------------------------------------------
    # 7️⃣ Subtopic Auto Decay
    # -----------------------------------------------------
    subtopics = (
        db.query(Subtopic)
        .filter(Subtopic.skill_id == skill.id)
        .all()
    )

    for sub in subtopics:

        if sub.last_practiced:
            sub_days = (today - sub.last_practiced).days
        else:
            sub_days = (today - skill.learned_date).days

        daily_decay_rate = 0.02
        decay = min(sub_days * daily_decay_rate, 50)

        new_health = max(0, sub.health_score - decay)
        sub.health_score = round(new_health, 2)

    db.commit()

    return score