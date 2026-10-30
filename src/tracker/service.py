"""Логика команд трекера."""

from datetime import date, datetime

from .models import Task
from .storage import Storage


class TrackerService:
    def __init__(self, storage: Storage):
        self.storage = storage

    @staticmethod
    def _next_id(tasks: list[Task]) -> int:
        return max((task.id for task in tasks), default=0) + 1

    def add(
        self,
        title: str,
        labels: list[str] | None = None,
        assignee: str | None = None,
        due: date | None = None,
    ) -> Task:
        tasks = self.storage.load()
        task = Task(
            id=self._next_id(tasks),
            title=title,
            labels=list(labels or []),
            assignee=assignee,
            due=due,
        )
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list_tasks(self) -> list[Task]:
        return [task for task in self.storage.load() if task.deleted_at is None]

    def _find_active(self, tasks: list[Task], task_id: int) -> Task:
        for task in tasks:
            if task.id == task_id and task.deleted_at is None:
                return task
        raise ValueError(f"задача {task_id} не найдена")

    def mark_done(self, task_id: int) -> Task:
        tasks = self.storage.load()
        task = self._find_active(tasks, task_id)
        task.done = True
        self.storage.save(tasks)
        return task

    def delete(self, task_id: int) -> Task:
        tasks = self.storage.load()
        task = self._find_active(tasks, task_id)
        task.deleted_at = datetime.now()
        self.storage.save(tasks)
        return task
