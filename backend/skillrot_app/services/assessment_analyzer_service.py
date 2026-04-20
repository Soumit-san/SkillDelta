import re
from typing import Dict, List
from skillrot_app.llm.llm_client import call_llm


# ============================================================
# 1️⃣ STRUCTURED SCORE PARSER (Highest confidence)
# ============================================================

def extract_topic_scores(text: str) -> Dict[str, float]:
    pattern = r"([A-Za-z][A-Za-z\s]{2,40})[\:\-]\s*(\d{1,3})%?"
    matches = re.findall(pattern, text)

    weak = {}

    for topic, score in matches:
        score = int(score)
        if 0 <= score <= 100 and score < 50:
            weakness_score = 1 - (score / 100)
            weak[topic.strip()] = round(weakness_score, 2)

    return weak


# ============================================================
# 2️⃣ GENERIC WRONG QUESTION DETECTOR
# ============================================================

def extract_wrong_question_blocks(text: str) -> List[str]:
    """
    Extract question blocks marked wrong (X Q1, X Q2 etc.)
    Works for any subject.
    """

    wrong_blocks = re.findall(
        r"X\s*Q\d+.*?(?=X\s*Q\d+|Y\s*Q\d+|VY\s*Q\d+|$)",
        text,
        re.DOTALL
    )

    return wrong_blocks


# ============================================================
# 3️⃣ LLM TOPIC CLASSIFIER
# ============================================================

def classify_question_topic(question_text: str, skill_context: str) -> str:
    """
    Use LLM to classify topic of a single question.
    """

    prompt = f"""
You are an academic topic classifier. You are specifically grading an assessment for the skill/course: "{skill_context}".

Identify the core subject topic of this question. 
CRITICAL: The topic MUST be related to "{skill_context}". If it is completely unrelated, return "IRRELEVANT_TOPIC".

Return ONLY a short topic name (2-4 words).
No explanation.

Question:
{question_text}
"""

    response = call_llm(prompt)

    if not response:
        return "General Concept"

    return response.strip().split("\n")[0]


# ============================================================
# 4️⃣ MASTER QUIZ ANALYZER (GENERALIZED)
# ============================================================

def analyze_quiz_with_llm(text: str, skill_context: str) -> Dict[str, float]:

    weak = {}

    wrong_questions = extract_wrong_question_blocks(text)

    if not wrong_questions:
        return weak

    for question in wrong_questions:

        topic = classify_question_topic(question, skill_context)

        if topic and topic != "IRRELEVANT_TOPIC":
            weak[topic] = 0.75  # moderate weakness

    return weak


# ============================================================
# MASTER ANALYZER
# ============================================================

def analyze_assessment_text(text: str, skill_name: str) -> Dict[str, float]:

    # 1️⃣ Structured score sheet
    weak = extract_topic_scores(text)
    if weak:
        return weak

    # 2️⃣ Quiz detection (generalized)
    weak = analyze_quiz_with_llm(text, skill_name)
    if weak:
        return weak

    return {}