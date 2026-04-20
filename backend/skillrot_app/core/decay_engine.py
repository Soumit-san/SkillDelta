import math

BASE_DECAY_RATE = 0.003
MAX_DECAY_DAYS = 365
MAX_HEALTH = 100
MIN_HEALTH = 0
RECOVERY_RATE = 0.15  # 15% gap closure per practice session

def compute_decay_score(
    days_since_last_record: int,
    days_since_learned: int,
    usage_frequency: float,
    skill_level: str,
    previous_health: float = None,
    sessions_today: int = 0
) -> float:
    """
    Cognitive Skill Model (Final Scalable Version)
    - Exponential forgetting from strictly recorded anchors
    - Gap closure recovery to safely scale past baseline towards 100
    - Idempotent deterministic session compounding
    """
    baseline_map = {
        "beginner": 60,
        "intermediate": 75,
        "advanced": 90
    }
    baseline = baseline_map.get(skill_level.lower() if skill_level else "intermediate", 75)

    # 1. Establish the Anchor (the precise health before today's interactions)
    if previous_health is None:
        effective_days = min(max(0, days_since_learned), MAX_DECAY_DAYS)
        anchor_health = baseline * math.exp(-BASE_DECAY_RATE * effective_days)
    else:
        effective_days = min(max(0, days_since_last_record), MAX_DECAY_DAYS)
        anchor_health = previous_health * math.exp(-BASE_DECAY_RATE * effective_days)

    health = anchor_health

    # 2. Compounding Practice Boosts (Idempotent for today)
    for _ in range(sessions_today):
        health += RECOVERY_RATE * (MAX_HEALTH - health)

    # 3. Add Consistency Bonus (only applied on active practice days)
    if sessions_today > 0:
        usage_bonus = min(usage_frequency * 3, 5)
        health += usage_bonus

    return round(max(MIN_HEALTH, min(MAX_HEALTH, health)), 2)