"""Данные, с которыми приложение стартует, и учётные данные для входа.

Приложение хранит записи в памяти браузера, поэтому каждый тест начинает
с одного и того же набора.
"""

USERNAME = "admin"
PASSWORD = "secret"

MENU = ["Dashboard", "Tasks", "Users", "Labels", "Task statuses"]

USER_EMAILS = [
    "john@google.com",
    "jack@yahoo.com",
    "jane@gmail.com",
    "alice@hotmail.com",
    "peter@outlook.com",
    "sarah@example.com",
    "michael@example.com",
    "emily@example.com",
]

STATUSES = {
    "Draft": "draft",
    "To Review": "to_review",
    "To Be Fixed": "to_be_fixed",
    "To Publish": "to_publish",
    "Published": "published",
}

LABELS = ["bug", "feature", "enhancement", "task", "critical"]

TASKS_BY_STATUS = {
    "Draft": ["Task 11", "Task 5", "Task 6"],
    "To Review": ["Task 2", "Task 12", "Task 7"],
    "To Be Fixed": ["Task 1", "Task 13", "Task 8"],
    "To Publish": ["Task 3", "Task 14", "Task 9"],
    "Published": ["Task 4", "Task 15", "Task 10"],
}

TASKS_OF_JOHN = ["Task 1", "Task 2", "Task 5", "Task 11", "Task 15"]
