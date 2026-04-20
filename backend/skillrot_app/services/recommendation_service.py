from skillrot_app.services.youtube_service import fetch_youtube_videos
from skillrot_app.services.plan_service import generate_refresh_plan
from skillrot_app.llm.llm_client import call_llm
from skillrot_app.llm.prompt_builder import build_prompt
from skillrot_app.services.wikipedia_service import fetch_wikipedia_article
from skillrot_app.models.subtopic import Subtopic  # 🔥 if you create subtopic model
from sqlalchemy.orm import Session

import json


# 🔹 STEP 1 — Convert Health → Learning Level
def health_to_level(health: float) -> str:
    if health < 40:
        return "beginner"
    elif health < 70:
        return "intermediate"
    else:
        return "advanced"


# 🔹 STEP 2 — Ask LLM for ONE weak subtopic
def get_weak_subtopic_from_llm(skill_name: str, level: str) -> str:

    prompt = f"""
    A student is at {level} level in {skill_name}.
    Suggest ONE specific subtopic they should revise first.
    Return only the topic name (2-4 words). No explanation.
    Do not use JSON formatting. Do not use brackets.
    """

    response = call_llm(prompt)

    if response:
        try:
            content = response["choices"][0]["message"]["content"].strip()
            topic = content.replace('"', '').replace('{', '').replace('}', '').replace('[', '').replace(']', '').strip()
            if len(topic) < 2:
                raise ValueError("Topic too short or empty")
            return topic
        except Exception:
            pass

    # 🔒 Safe fallback
    if level == "beginner":
        return f"{skill_name} fundamentals"
    elif level == "intermediate":
        return f"{skill_name} core concepts"
    else:
        return f"{skill_name} advanced topics"


# 🔹 STEP 3 — If subtopics exist, pick weakest
def get_weakest_subtopic_from_db(skill_id: int, db: Session):
    subtopics = (
        db.query(Subtopic)
        .filter(Subtopic.skill_id == skill_id)
        .order_by(Subtopic.health_score.asc())
        .all()
    )

    if subtopics:
        return subtopics[0].name  # weakest one

    return None


def generate_recommendation(skill, health, status, db: Session):

    # 🔹 STEP 1 — Convert health to level
    level = health_to_level(health)

    # 🔹 STEP 2 — Try DB subtopics first
    focus_topic = get_weakest_subtopic_from_db(skill.id, db)

    # 🔹 STEP 3 — If none exist, ask LLM
    if not focus_topic:
        focus_topic = get_weak_subtopic_from_llm(skill.name, level)

    # 🔹 STEP 4 — Fetch Resources

    youtube_resources = fetch_youtube_videos(focus_topic, skill.name, max_results=3)
    wiki_article = fetch_wikipedia_article(focus_topic, skill.name)

    resources = []

    # 🔥 Enforce order: Videos first
    if youtube_resources:
        resources.extend(youtube_resources[:3])

    if wiki_article:
        resources.append(wiki_article)

    # 🔹 STEP 5 — Generate Study Plan
    plan = generate_refresh_plan(status, health)

    # 🔹 STEP 6 — Explanation LLM
    explanation_prompt = build_prompt(skill.name, health, status, resources)
    explanation_response = call_llm(explanation_prompt)

    reason = None
    tips = None

    if explanation_response:
        try:
            content = explanation_response["choices"][0]["message"]["content"]
            data = json.loads(content)

            reason = data.get("reason")
            tips = data.get("tips")

        except Exception:
            pass

    # 🔒 Safe fallback explanation
    if not reason:
        if status == "Stable":
            reason = "The skill is well-maintained with consistent recent practice."
            tips = [
                "Continue light periodic practice",
                "Occasionally revise fundamentals"
            ]

        elif status == "At-Risk":
            reason = "The skill shows early signs of decay due to reduced recent practice."
            tips = [
                "Increase practice frequency",
                "Revise key concepts",
                "Apply the skill in short exercises"
            ]

        else:
            reason = "The skill has significantly decayed due to prolonged inactivity."
            tips = [
                "Restart with core fundamentals",
                "Practice daily with structured sessions",
                "Rebuild conceptual understanding"
            ]

    return {
        "skill": skill.name,
        "health": health,
        "level": level,
        "focus_topic": focus_topic,  # 🔥 dynamic + DB aware
        "status": status,
        "reason": reason,
        "tips": tips,
        "resources": resources,
        "plan": plan
    }