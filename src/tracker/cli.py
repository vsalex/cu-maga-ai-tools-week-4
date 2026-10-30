"""Разбор аргументов через argparse и запуск команд."""

import argparse
import sys
from datetime import date

from .service import TrackerService
from .storage import Storage


def _parse_due(value: str) -> date:
    return date.fromisoformat(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tracker", description="Консольный трекер задач")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="добавить задачу")
    add.add_argument("title", help="заголовок задачи")
    add.add_argument("--labels", help="метки через запятую", default="")
    add.add_argument("--assignee", help="исполнитель", default=None)
    add.add_argument("--due", help="срок YYYY-MM-DD", type=_parse_due, default=None)

    sub.add_parser("list", help="показать активные задачи")

    done = sub.add_parser("done", help="отметить задачу выполненной")
    done.add_argument("id", type=int, help="идентификатор задачи")

    delete = sub.add_parser("delete", help="удалить задачу (мягко)")
    delete.add_argument("id", type=int, help="идентификатор задачи")

    return parser


def _format(task) -> str:
    status = "[x]" if task.done else "[ ]"
    parts = [f"{task.id}. {status} {task.title}"]
    if task.labels:
        parts.append(f" [{', '.join(task.labels)}]")
    if task.assignee:
        parts.append(f" @{task.assignee}")
    if task.due:
        parts.append(f" due {task.due.isoformat()}")
    return "".join(parts)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = TrackerService(Storage())

    try:
        if args.command == "add":
            labels = [item.strip() for item in args.labels.split(",") if item.strip()]
            task = service.add(args.title, labels=labels, assignee=args.assignee, due=args.due)
            print(f"добавлена задача {task.id}: {task.title}")
        elif args.command == "list":
            tasks = service.list_tasks()
            if not tasks:
                print("нет активных задач")
            else:
                for task in tasks:
                    print(_format(task))
        elif args.command == "done":
            task = service.mark_done(args.id)
            print(f"задача {task.id} отмечена выполненной")
        elif args.command == "delete":
            task = service.delete(args.id)
            print(f"задача {task.id} удалена")
    except ValueError as exc:
        print(f"ошибка: {exc}", file=sys.stderr)
        return 1

    return 0
