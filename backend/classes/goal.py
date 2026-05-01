# backend/classes/goal.py

# utility
from dataclasses import dataclass
from datetime import date


@dataclass
class Goal:
    # because SQLite assigns this
    id: int | None
    location: str
    due: date
    action: str
    completed: bool = False

    def display(self) -> str:
        return f"{self.action} | {self.location} | {self.due.isoformat()}"

    # future possibility of validating behaviors & locations
    def validate(self):
        if not self.location.strip():
            raise ValueError("Location is required.")

        if not self.action.strip():
            raise ValueError("Action is required.")

        if not isinstance(self.due, date):
            raise ValueError("Due date must be a date object.")


