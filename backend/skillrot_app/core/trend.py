def compute_trend(scores: list[float]) -> float:
    if len(scores) < 2:
        return 0.0

    return round(scores[-1] - scores[0], 2)
