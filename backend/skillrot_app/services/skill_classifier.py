def classify_skill(skill_name: str) -> str:
    name = skill_name.lower()

    programming_keywords = [
        "python", "java", "c++", "c#", "javascript", "js",
        "react", "node", "django", "flask", "html", "css"
    ]

    ml_keywords = [
        "machine learning", "ml", "deep learning", "dl",
        "artificial intelligence", "ai", "data science"
    ]

    performing_keywords = [
        "singing", "music", "guitar", "dance", "classical",
        "skating", "instrument"
    ]

    soft_skill_keywords = [
        "public speaking", "communication", "leadership",
        "confidence", "presentation"
    ]

    if any(k in name for k in programming_keywords):
        return "programming"

    if any(k in name for k in ml_keywords):
        return "machine_learning"

    if any(k in name for k in performing_keywords):
        return "performing_arts"

    if any(k in name for k in soft_skill_keywords):
        return "soft_skill"

    return "general"