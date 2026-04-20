def classify_skill(score: float) -> str:
    if score >= 80:
        return "Stable"
    elif score >= 60:
        return "At-Risk"
    else:
        return "Critical"
