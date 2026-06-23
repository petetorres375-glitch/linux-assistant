# linux_assistant

A Python tool that takes a Linux problem described in plain English and returns the recommended command, an explanation of what it does, and any warnings to be aware of. Runs as a web app or from the command line.

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

**Web app:**

```bash
python app.py
```

Open `http://localhost:5051`, describe your problem, and get results in the browser.

**CLI:**

```bash
python main.py
```

Type your issue in plain English at the prompt. Type `exit` or `quit` to close.

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

## Live Demo

[https://web-production-58a9b.up.railway.app/](https://web-production-58a9b.up.railway.app/)

## Deploy to Railway

1. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
2. Select this repository
3. Add environment variables: `GEMINI_API_KEY` and `SECRET_KEY`
4. Railway detects the `Procfile` and deploys automatically
