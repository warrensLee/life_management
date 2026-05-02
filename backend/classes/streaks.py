# models/streaks.py
from dataclasses import dataclass
from datetime import date, time

# what makes a streak?
#   1 id
#   2 days comppleted consecutively
#   3 some action
#   4 some (optional) time
#   5 some (optional) location
#   6 flag for completed today or not
#   7 created_at
#   8 updated_at
#   9 ended_at (if ended, otherwise null)

@dataclass
class Streak:
    id: int
    title: str
    description: str
    created_at: date
    updated_at: date
    ended_at: date | None = None
    completed: int = 0
    days_completed: int = 0

    def display(self) -> str:
        return f"{self.days_completed} | {self.title} | {self.description} | {self.completed}"

    # future possibility of validating behaviors & locations
    def validate(self):
        pass
