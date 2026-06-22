# linux_assistant

A Python CLI tool that takes a Linux problem described in plain English and returns the recommended command, an explanation of what it does, and any warnings to be aware of.

## Output

- **Command** — the recommended Linux command or sequence
- **Explanation** — plain-English breakdown of what it does and why
- **Warnings** — side effects, risks, or things to watch out for

## Requirements

- Python 3.12+
- A free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

## Setup

```bash
git clone https://github.com/petetorres375-glitch/linux-assistant.git
cd linux_assistant

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Gemini API key
```

## Usage

```bash
python main.py
```

Type your issue in plain English at the `Describe your issue:` prompt. Type `exit` or `quit` to close.

## Example

```
Problem: I want to find all .log files older than 7 days and delete them

Command:  find /path/to/logs -name "*.log" -mtime +7 -delete
Explanation: The find command searches for files matching *.log that were
             last modified more than 7 days ago and deletes them in place.
Warnings:  • -delete is permanent. There is no undo.
           • Test first with -print instead of -delete to preview matches.
```

## Model

Uses `gemini-2.5-flash` as the primary model. Automatically falls back to `gemini-2.5-flash-lite` on a 503 (model overload) before giving up.

## Logs

All queries and returned commands are saved to `logs/queries.log`.
