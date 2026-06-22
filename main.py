#!/usr/bin/env python3
"""linux_assistant — Describe a Linux problem, get the command, explanation, and warnings."""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

load_dotenv()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "queries.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

console = Console()

SYSTEM_PROMPT = """\
You are a Linux command-line expert. The user will describe a problem or task in plain English.
Return a JSON object with exactly these three keys:
- "command": The recommended Linux command or sequence of commands (as a string).
- "explanation": A plain-English explanation of what the command does and why it works.
- "warnings": A list of cautions or side effects the user should know. If none, return ["None."].

Return only valid JSON. No markdown fences, no extra text.
"""


def ask(problem: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]GEMINI_API_KEY not set in .env[/red]")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    with console.status("Thinking...", spinner="dots"):
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"{SYSTEM_PROMPT}\n\nProblem: {problem}",
        )

    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


def display(result: dict) -> None:
    console.print(Panel(
        f"[bold green]{result.get('command', '')}[/bold green]",
        title="[bold]Command[/bold]",
        border_style="green",
    ))
    console.print(Panel(
        result.get("explanation", ""),
        title="[bold]Explanation[/bold]",
        border_style="cyan",
    ))
    warnings = result.get("warnings", [])
    warning_text = "\n".join(f"• {w}" for w in warnings)
    console.print(Panel(
        warning_text,
        title="[bold]Warnings[/bold]",
        border_style="yellow",
    ))


def main():
    console.print(Panel(
        "[bold]Linux Assistant[/bold]\nDescribe your problem in plain English.",
        border_style="white",
    ))

    while True:
        try:
            problem = Prompt.ask("\n[bold cyan]>[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Bye.[/dim]")
            break

        if not problem:
            continue

        if problem.lower() in {"exit", "quit", "q"}:
            console.print("[dim]Bye.[/dim]")
            break

        result = ask(problem)
        display(result)
        logging.info("Q: %s | CMD: %s", problem, result.get("command", ""))


if __name__ == "__main__":
    main()
