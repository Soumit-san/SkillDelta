from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.models.user import User
from skillrot_app.models.skill import Skill
from skillrot_app.services.recommendation_service import generate_recommendation
from skillrot_app.api.analysis import get_skill_health
from skillrot_app.core.skill_analyzer import classify_skill
from skillrot_app.core.security import get_current_user

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

# In-memory cache keyed by "skill_id_health". 
# Automatically invalidates/refreshes when health changes from practice, decay, or assessments.
_rec_cache = {}

def clear_recommendation_cache(skill_id: int):
    keys_to_delete = [k for k in _rec_cache.keys() if k.startswith(f"{skill_id}_")]
    for k in keys_to_delete:
        del _rec_cache[k]

@router.get("/skills/{skill_id}")
def recommend_for_skill(skill_id: int, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    health_data = get_skill_health(skill_id, db)
    health = health_data["health"]
    status = classify_skill(health)

    cache_key = f"{skill_id}_{health}"
    if cache_key in _rec_cache:
        return _rec_cache[cache_key]

    recommendation = generate_recommendation(skill, health, status, db)
    _rec_cache[cache_key] = recommendation
    return recommendation


@router.get("")
def get_all_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate recommendations for all skills owned by the current user.
    """
    skills = db.query(Skill).filter(Skill.user_id == current_user.id).all()
    all_recommendations = []
    
    for skill in skills:
        health_data = get_skill_health(skill.id, db)
        health = health_data["health"]
        status = classify_skill(health)
        
        # We append a wrapper around the output so we know which skill it belongs to
        rec = generate_recommendation(skill, health, status, db)
        # Assuming generate_recommendation returns a list of dictionaries
        if isinstance(rec, list):
            for r in rec:
                r["skill_name"] = skill.name
                all_recommendations.append(r)
        elif isinstance(rec, dict):
            rec["skill_name"] = skill.name
            all_recommendations.append(rec)
            
    return all_recommendations