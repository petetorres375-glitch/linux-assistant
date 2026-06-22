#!/usr/bin/env python3
"""linux_assistant — Describe a Linux problem, get the command, explanation, and warnings."""

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from ai import ask

load_dotenv()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "queries.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

console = Console()


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
    warning_text = "\n".join(f"• {w}" for w in result.get("warnings", []))
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
            problem = Prompt.ask("\n[bold cyan]Describe your issue[/bold cyan]").strip()
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
