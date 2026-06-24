"""Shared Claude AI logic for linux_assistant."""

import json

import anthropic

SYSTEM_PROMPT = """\
You are a Linux command-line expert. The user will describe a problem or task in plain English.
Return a JSON object with exactly these three keys:
- "command": The recommended Linux command or sequence of commands (as a string).
- "explanation": A plain-English explanation of what the command does and why it works.
- "warnings": A list of cautions or side effects the user should know. If none, return ["None."].

Return only valid JSON. No markdown fences, no extra text.
"""

MODEL = "claude-haiku-4-5-20251001"


def ask(problem: str) -> dict:
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": f"Problem: {problem}"}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)
