"""Shared Gemini AI logic for linux_assistant."""

import json
import os

from google import genai
from google.genai import errors as genai_errors

SYSTEM_PROMPT = """\
You are a Linux command-line expert. The user will describe a problem or task in plain English.
Return a JSON object with exactly these three keys:
- "command": The recommended Linux command or sequence of commands (as a string).
- "explanation": A plain-English explanation of what the command does and why it works.
- "warnings": A list of cautions or side effects the user should know. If none, return ["None."].

Return only valid JSON. No markdown fences, no extra text.
"""

MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]


def ask(problem: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in .env")

    client = genai.Client(api_key=api_key)

    for i, model in enumerate(MODELS):
        try:
            response = client.models.generate_content(
                model=model,
                contents=f"{SYSTEM_PROMPT}\n\nProblem: {problem}",
            )
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(raw)
        except genai_errors.ServerError as e:
            if "503" in str(e) and i < len(MODELS) - 1:
                continue
            raise
