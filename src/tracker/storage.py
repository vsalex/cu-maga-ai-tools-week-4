"""Чтение и запись tasks.json."""

import json
from pathlib import Path

from .models import Task

DEFAULT_PATH = Path("tasks.json")


class Storage:
    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = path

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task.from_dict(item) for item in data]

    def save(self, tasks: list[Task]) -> None:
        payload = [task.to_dict() for task in tasks]
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
