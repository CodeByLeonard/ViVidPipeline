import json
from pathlib import Path

def status(path: str):
    if not Path(path).exists():
        return {}

    with open(file="./sessions/sre/session.json", mode="r") as f:
        return json.load(f)