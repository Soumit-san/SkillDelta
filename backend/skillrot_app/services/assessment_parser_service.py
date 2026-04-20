import re
import json
from typing import Dict, List
from skillrot_app.llm.llm_client import call_llm


# ============================================================
# 🔹 1️⃣ STRUCTURED SCORE PARSER
# ============================================================

def parse_structured_scores(text: str) -> Dict[str, float]:
    """
    Handles:
    Recursion: 30%
    Sorting - 80%
    DP: 40
    """

    pattern = r"([A-Za-z][A-Za-z\s]{2,40})[\:\-]\s*(\d{1,3})%?"
    matches = re.findall(pattern, text)

    weak = {}

    for topic, score in matches:
        score = int(score)
        if 0 <= score <= 100 and score < 50:
            weakness = round(1 - (score / 100), 2)
            weak[topic.strip()] = weakness

    return weak


# ============================================================
# 🔹 2️⃣ QUIZ / VERDICT PARSER
# ============================================================

def parse_quiz_mistakes(text: str) -> List[str]:
    """
    Detect incorrect / wrong / TLE etc.
    """

    text_lower = text.lower()

    mistake_signals = [
        "incorrect",
        "wrong",
        "time limit exceeded",
        "runtime error",
        "compilation error",
        "failed",
        "wrong answer"
    ]

    if any(signal in text_lower for signal in mistake_signals):
        return [text]  # send full text to LLM for topic abstraction

    return []


# ============================================================
# 🔹 3️⃣ CONTROLLED LLM TOPIC EXTRACTION
# ============================================================

def extract_topics_with_llm(text: str) -> Dict[str, float]:

    prompt = f"""
You are analyzing a student's test performance.

Extract ONLY conceptual weak topics.

DO NOT return sentences.
DO NOT return question fragments.

Return STRICT JSON:

{{
  "weak_subtopics": [
    {{
      "topic": "Normalization",
      "severity": 0.8
    }}
  ]
}}

If student performed well overall, return:

{{
  "weak_subtopics": []
}}

Content:
{text}
"""

    response = call_llm(prompt)

    if not response:
        return {}

    try:
        data = json.loads(response)
        result = {}

        for item in data.get("weak_subtopics", []):
            topic = item.get("topic")
            severity = item.get("severity")

            if (
                isinstance(topic, str)
                and isinstance(severity, (int, float))
                and 0 <= severity <= 1
            ):
                result[topic.strip()] = round(float(severity), 2)

        return result

    except:
        return {}