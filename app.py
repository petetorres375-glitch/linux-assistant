"""linux_assistant — Flask web interface."""

import logging
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request

from ai import ask

load_dotenv()

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "queries.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    problem = ""
    error = None

    if request.method == "POST":
        problem = request.form.get("problem", "").strip()
        if problem:
            try:
                result = ask(problem)
                logging.info("WEB Q: %s | CMD: %s", problem, result.get("command", ""))
            except Exception as e:
                error = str(e)

    return render_template("index.html", problem=problem, result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5051)
