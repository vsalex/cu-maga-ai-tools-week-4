# Трекер задач

Консольный трекер задач на Python 3.11+. Задачи хранятся в файле `tasks.json`, удаление мягкое: записи не исчезают, а помечаются отметкой.

## Установка

```bash
make setup
source .venv/bin/activate
```

## Команды

После активации окружения доступна команда `tracker`.

Добавить задачу:

```bash
tracker add "Отчёт" --labels urgent,work --assignee Саша --due 2026-11-01
tracker add "Созвон"
```

Показать активные задачи:

```bash
tracker list
```

Отметить задачу выполненной:

```bash
tracker done 1
```

Удалить задачу:

```bash
tracker delete 2
```

`delete` — мягкое удаление: запись остаётся в `tasks.json` с заполненным полем `deleted_at`, а в `list` задача больше не показывается.

## Тесты

```bash
make check
```

## Выход из окружения

```bash
deactivate
```
