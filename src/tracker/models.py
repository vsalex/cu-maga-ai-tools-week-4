"""Модель задачи и её сериализация в/из JSON."""

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Task:
    id: int
    title: str
    labels: list[str] = field(default_factory=list)
    assignee: str | None = None
    due: date | None = None
    done: bool = False
    deleted_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "labels": self.labels,
            "assignee": self.assignee,
            "due": self.due.isoformat() if self.due else None,
            "done": self.done,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        due = data.get("due")
        deleted_at = data.get("deleted_at")
        return cls(
            id=data["id"],
            title=data["title"],
            labels=list(data.get("labels", [])),
            assignee=data.get("assignee"),
            due=date.fromisoformat(due) if due else None,
            done=bool(data.get("done", False)),
            deleted_at=datetime.fromisoformat(deleted_at) if deleted_at else None,
        )
