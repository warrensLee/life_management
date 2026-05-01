# core/personality.py
from dataclasses import dataclass



@dataclass
class Personality:
    # because SQLite assigns this
    id: int | None
    pillar: str
    other_example: str
    personal_example: str



    def display(self) -> str:
        return f"{self.pillar} ==> {self.other_example} ==> {self.personal_example}"

    # future possibility of validating if block code is chosen instead
    def validate(self):
        pass