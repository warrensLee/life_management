# core/services.py
from datetime import datetime
from backend.classes.goal import Goal
# core/services.py
from backend import database
from backend.classes.goal import Goal
from datetime import datetime


def parse_due_date(s: str):
    return datetime.strptime(s.strip(), "%Y-%m-%d").date()


def validate_fields(location: str, due_str: str, action: str):
    if not location.strip():
        raise ValueError("Location is required.")
    if not action.strip():
        raise ValueError("Action/behavior is required.")
    # will throw if invalid
    parse_due_date(due_str)
