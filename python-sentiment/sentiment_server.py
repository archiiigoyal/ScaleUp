from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from intent_detector import detect_intents
from query_grouper import group_queries
from descriptive_grouper import group_descriptive
from llm_generator import build_prompt, generate_insight  # ✅ UPDATED

app = FastAPI()


class AnalyzeRequest(BaseModel):
    comments: List[str]


@app.post("/analyze-competitor")
def analyze(payload: AnalyzeRequest):

    intents = detect_intents(payload.comments)

    grouped = {
        "queries": group_queries(intents["queries"]),
        "descriptive": group_descriptive(intents["descriptive"])
    }

    prompt = build_prompt(grouped)

    insight = generate_insight(prompt)

    return {
        "insight": insight
    }
