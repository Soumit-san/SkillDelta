def generate_refresh_plan(status: str, health: float) -> dict:
    """
    Smart adaptive plan based on status + exact health.
    """

    if status == "Stable":
        if health > 85:
            return {"days": 2, "minutes_per_day": 10}
        else:
            return {"days": 3, "minutes_per_day": 15}

    elif status == "At-Risk":
        if health > 60:
            return {"days": 5, "minutes_per_day": 25}
        else:
            return {"days": 7, "minutes_per_day": 30}

    else:  # Critical
        if health > 20:
            return {"days": 10, "minutes_per_day": 40}
        else:
            return {"days": 14, "minutes_per_day": 45}