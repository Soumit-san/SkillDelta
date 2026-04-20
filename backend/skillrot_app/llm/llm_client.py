import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_ENABLED = os.getenv("LLM_ENABLED", "false").lower() == "true"

client = Groq(api_key=GROQ_API_KEY)

def call_llm(prompt: str):
    """
    Calls Groq LLM (LLaMA/Mixtral).
    Returns plain text response or None.
    """

    if not LLM_ENABLED or not GROQ_API_KEY:
        return None

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an educational assistant. Return only clean JSON when asked."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )

        content = completion.choices[0].message.content.strip()

        # Remove accidental markdown formatting
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return content

    except Exception as e:
        print("Groq LLM error:", e)
        return None