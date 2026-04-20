"""
skillrot_app/api/role_filter.py

FastAPI router that exposes role-based skill filtering and sorting.
Follows the same pattern as your existing skills.py router.

Endpoints added:
  GET  /skills/roles                          → list all available roles
  GET  /skills/filter?role=cybersecurity      → user's skills sorted by role priority
  GET  /skills/filter?role=cybersecurity&priority=1  → filter to a specific priority level
"""

from typing import List, Optional, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from skillrot_app.db.database import get_db
from skillrot_app.core.security import get_current_user
from skillrot_app.models.user import User
from skillrot_app.models.skill import Skill
from skillrot_app.models.skill_history import SkillHistory
from skillrot_app.models.skill_health_history import SkillHealthHistory
from skillrot_app.data.role_skills import ROLES, PRIORITY_META
from skillrot_app.services.role_filter_service import (
    sort_skills_by_priority,
    filter_skills_by_priority,
    get_all_roles_summary,
)
from datetime import date

router = APIRouter(prefix="/skills", tags=["Role Filter"])





@router.get("/roles", summary="List all predefined roles with skill counts")
def list_roles() -> List[Dict[str, Any]]:
    """
    Returns all available predefined roles and their priority breakdown.
    No auth required — this is static reference data.

    Response example:
    [
      {
        "key": "cybersecurity",
        "label": "Cybersecurity",
        "icon": "🔐",
        "skill_count": 16,
        "priorities": {
          "1": {"label": "Critical", "count": 2},
          ...
        }
      },
      ...
    ]
    """
    return get_all_roles_summary()


@router.get("/filter", summary="Get user skills sorted and filtered by role priority")
def filter_skills_by_role(
    role: str = Query(
        ...,
        description="Role key, e.g. cybersecurity, software_engineering, data_science, devops, web_development, ml_engineering",
    ),
    priority: Optional[int] = Query(
        default=None,
        ge=1,
        le=5,
        description="Filter to a specific priority level (1=Critical … 5=Optional). Omit to return all priorities sorted.",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Returns the current user's skills sorted by their importance in the given role.

    - **role**: must be a valid key from GET /skills/roles
    - **priority**: optional filter — only return skills at this priority level

    Each skill in the response gets two extra fields:
    - `role_priority` (int 1–5, or null if not mapped to this role)
    - `role_priority_label` (e.g. "Critical", "High", "Unranked")

    Skills not recognised in the role are sorted to the end (Unranked).
    """
    if role not in ROLES:
        valid = ", ".join(ROLES.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role '{role}'. Valid roles: {valid}",
        )

    # Fetch this user's skills from DB
    db_skills: List[Skill] = (
        db.query(Skill)
        .filter(Skill.user_id == current_user.id)
        .all()
    )

    if not db_skills:
        return {
            "role":        role,
            "role_label":  ROLES[role]["label"],
            "priority":    priority,
            "total":       0,
            "skills":      [],
        }

    today = date.today()
    skill_ids = [s.id for s in db_skills]

    # Bulk fetch health
    health_records = (
        db.query(SkillHealthHistory)
        .filter(SkillHealthHistory.skill_id.in_(skill_ids))
        .order_by(SkillHealthHistory.skill_id, SkillHealthHistory.recorded_at.desc())
        .all()
    )
    health_map = {}
    for h in health_records:
        if h.skill_id not in health_map:
            health_map[h.skill_id] = []
        health_map[h.skill_id].append(h)

    # Bulk fetch history
    practice_history = (
        db.query(SkillHistory)
        .filter(SkillHistory.skill_id.in_(skill_ids))
        .order_by(SkillHistory.skill_id, SkillHistory.date.desc())
        .all()
    )
    history_map = {}
    for ph in practice_history:
        if ph.skill_id not in history_map:
            history_map[ph.skill_id] = []
        history_map[ph.skill_id].append(ph)

    skill_dicts = []
    for skill in db_skills:
        # Get health
        s_health_records = health_map.get(skill.id, [])
        if s_health_records:
            health = s_health_records[0].health
            days_since = (today - s_health_records[0].recorded_at.date()).days
            if days_since > 0:
                 health = max(0, health - (days_since * 0.5))
        else:
            health = 100.0
            
        health = round(health, 2)

        # Get last practiced
        s_history = history_map.get(skill.id, [])
        if s_history:
            last_practiced = s_history[0].date.isoformat()
        else:
            last_practiced = skill.learned_date.isoformat() if skill.learned_date else None

        skill_dicts.append({
            "id":           str(skill.id),
            "name":         skill.name,
            "level":        skill.level,
            "health":       health,
            "last_practiced": last_practiced,
            "learned_date": skill.learned_date.isoformat() if skill.learned_date else None,
            "created_at":   skill.created_at.isoformat() if skill.created_at else None,
        })

    # Sort or filter via service layer
    if priority is not None:
        result = filter_skills_by_priority(skill_dicts, role, priority)
    else:
        result = sort_skills_by_priority(skill_dicts, role)
        # Filter out skills that are not related to this role at all
        result = [s for s in result if s.get("role_priority") is not None]

    return {
        "role":        role,
        "role_label":  ROLES[role]["label"],
        "priority":    priority,
        "priority_label": PRIORITY_META[priority]["label"] if priority else None,
        "total":       len(result),
        "skills":      result,
    }


@router.get("/roles/{role_key}/skills", summary="List all expected skills for a role with priority info")
def list_role_skills(role_key: str) -> Dict[str, Any]:
    """
    Returns the full ranked skill list for a given role — not the user's skills,
    but the reference list. Useful for the frontend to show what skills matter
    for a role even before the user has added them.

    No auth required.
    """
    if role_key not in ROLES:
        valid = ", ".join(ROLES.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role '{role_key}'. Valid roles: {valid}",
        )

    role_data = ROLES[role_key]
    skills_by_priority: Dict[str, List] = {str(p): [] for p in range(1, 6)}

    for skill in role_data["skills"]:
        skills_by_priority[str(skill.priority)].append({
            "name":           skill.name,
            "priority":       skill.priority,
            "priority_label": PRIORITY_META[skill.priority]["label"],
        })

    return {
        "role":              role_key,
        "label":             role_data["label"],
        "icon":              role_data["icon"],
        "skills_by_priority": skills_by_priority,
        "all_skills":        [
            {
                "name":           s.name,
                "priority":       s.priority,
                "priority_label": PRIORITY_META[s.priority]["label"],
            }
            for s in sorted(role_data["skills"], key=lambda x: x.priority)
        ],
    }