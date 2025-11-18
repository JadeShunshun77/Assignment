from dataclasses import dataclass
from typing import Optional


@dataclass
class Florist:
    name: str
    speciality: Optional[str] = None

    HOURS_PER_MONTH: int = 80
    MINUTES_PER_HOUR: int = 60

    def monthly_capacity_minutes(self) -> int:
        return self.HOURS_PER_MONTH * self.MINUTES_PER_HOUR

    def __repr__(self) -> str:
        if self.speciality:
            return f"{self.name} (speciality: {self.speciality})"
        return self.name
