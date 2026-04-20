from typing import List, Optional, Dict, Any
from skillrot_app.data.role_skills import ROLES, PRIORITY_META, RoleSkill


def _match_priority(skill_name: str, role_key: str) -> Optional[int]:
    if role_key not in ROLES:
        return None
    lower = skill_name.lower().strip()
    for rs in ROLES[role_key]["skills"]:
        rs_lower = rs.name.lower()
        if lower == rs_lower or rs_lower in lower or lower in rs_lower:
            return rs.priority
    return None


def get_priority_for_skill(skill_name: str, role_key: str) -> Optional[int]:
    return _match_priority(skill_name, role_key)


def enrich_skills_with_priority(
    skills: List[Dict[str, Any]],
    role_key: str,
    name_field: str = "name",
) -> List[Dict[str, Any]]:
    enriched = []
    for skill in skills:
        priority = _match_priority(skill.get(name_field, ""), role_key)
        meta = PRIORITY_META.get(priority, {"label": "Unranked"})
        enriched.append({**skill, "role_priority": priority, "role_priority_label": meta["label"]})
    return enriched


def sort_skills_by_priority(
    skills: List[Dict[str, Any]],
    role_key: str,
    name_field: str = "name",
    unranked_last: bool = True,
) -> List[Dict[str, Any]]:
    enriched = enrich_skills_with_priority(skills, role_key, name_field)
    return sorted(enriched, key=lambda s: s.get("role_priority") or (999 if unranked_last else 0))


def filter_skills_by_priority(
    skills: List[Dict[str, Any]],
    role_key: str,
    priority: Optional[int] = None,
    name_field: str = "name",
) -> List[Dict[str, Any]]:
    sorted_skills = sort_skills_by_priority(skills, role_key, name_field)
    if priority is None:
        return sorted_skills
    return [s for s in sorted_skills if s.get("role_priority") == priority]


def get_all_roles_summary() -> List[Dict[str, Any]]:
    return [
        {
            "key": key,
            "label": data["label"],
            "icon": data["icon"],
            "skill_count": len(data["skills"]),
            "priorities": {
                str(p): {
                    "label": PRIORITY_META[p]["label"],
                    "count": sum(1 for s in data["skills"] if s.priority == p),
                }
                for p in range(1, 6)
            },
        }
        for key, data in ROLES.items()
    ]
