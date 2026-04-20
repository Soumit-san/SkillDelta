def build_prompt(skill, health, status, resources):
    resource_text = "\n".join(
        [f"- {r['title']} ({r['type']})" for r in resources]
    )

    # Detect fallback resources
    is_generic = (
        not resources or
        resources[0].get("type") == "general"
    )

    resource_note = (
        "No specific curated resources were found. Using general learning guidance."
        if is_generic
        else "Curated learning resources are available."
    )

    # 🟢 STABLE
    if status == "Stable":
        return f"""
Skill: {skill}
Health: {health}%
Status: Stable

{resource_note}

Resources:
{resource_text}

Tasks:
1. Explain briefly why the skill is healthy.
2. Give 2 light maintenance tips.
3. Rank the resources for optional revision.

Return JSON with keys: reason, tips, ranked_resources.
"""

    # 🟡 AT-RISK
    if status == "At-Risk":
        return f"""
Skill: {skill}
Health: {health}%
Status: At-Risk

{resource_note}

Resources:
{resource_text}

Tasks:
1. Explain briefly why the skill is starting to decay.
2. Give 3 preventive improvement tips.
3. Rank the resources for quick recovery.

Return JSON with keys: reason, tips, ranked_resources.
"""

    # 🔴 CRITICAL
    return f"""
Skill: {skill}
Health: {health}%
Status: Critical

{resource_note}

Resources:
{resource_text}

Tasks:
1. Explain briefly why the skill has significantly decayed.
2. Give 3 urgent improvement tips.
3. Rank the resources for rapid recovery.

Return JSON with keys: reason, tips, ranked_resources.
"""
