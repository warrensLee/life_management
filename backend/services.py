# core/services.py
from datetime import datetime, date
from backend.classes.goal import Goal
# core/services.py
from backend import database
from backend.classes.goal import Goal


def parse_due_date(value):
    if not value:
        return None

    return date.fromisoformat(value[:10])


def validate_fields(location: str, due_str: str, action: str):
    if not location.strip():
        raise ValueError("Location is required.")
    if not action.strip():
        raise ValueError("Action/behavior is required.")
    # will throw if invalid
    parse_due_date(due_str)
