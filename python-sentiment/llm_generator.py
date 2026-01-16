import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a business analyst.
Analyze Instagram comments and extract:
1. Pricing concerns
2. Customer objections
3. Positive selling points
4. Actionable recommendations.

Return the output in bullet points.
"""

def build_prompt(grouped: dict) -> str:
    return json.dumps(
        {
            "queries": grouped.get("queries", {}),
            "descriptive_feedback": grouped.get("descriptive", {})
        },
        indent=2
    )

def generate_insight(prompt_json: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ UPDATED MODEL
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"DATA:\n{prompt_json}"}
        ],
        temperature=0.3,
        max_tokens=400
    )

    return completion.choices[0].message.content.strip()
