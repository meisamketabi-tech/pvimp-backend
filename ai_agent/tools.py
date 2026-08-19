import subprocess
import os
from config import PROJECT_PATH


ALLOWED = [
    "python scripts",
    "alembic",
    "pytest",
    "npm run",
    "git status",
    "git log",
]


def run_command(command):

    if not any(command.startswith(x) for x in ALLOWED):
        return "BLOCKED COMMAND"

    result = subprocess.run(
        command,
        cwd=PROJECT_PATH,
        shell=True,
        capture_output=True,
        text=True
    )

    return (
        result.stdout
        +
        "\n"
        +
        result.stderr
    )


def read_file(path):

    full = os.path.join(
        PROJECT_PATH,
        path
    )

    if not full.startswith(PROJECT_PATH):
        return "INVALID PATH"

    with open(full, encoding="utf-8") as f:
        return f.read()