# models/streaks.py
from dataclasses import dataclass
from datetime import date, time

# what makes a streak_completion?
#   1 id: int
#   2 streak_id: int
#   3 completed_date: date

@dataclass
class Streak:
    id: int
    streak_id: int
    completed_date: date

    # future possibility of validating behaviors & locations
    def validate(self):
        pass
