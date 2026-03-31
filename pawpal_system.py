from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

@dataclass
class Owner:
    name: str
    available_minutes: int = 8 * 60
    preferences: Dict[str, str] = field(default_factory=dict)

    def update_availability(self, minutes: int) -> None:
        self.available_minutes = minutes

    def set_preference(self, key: str, value: str) -> None:
        self.preferences[key] = value

@dataclass
class Pet:
    name: str
    species: str = "dog"
    needs: List[str] = field(default_factory=list)

    def add_need(self, need: str) -> None:
        self.needs.append(need)

    def remove_need(self, need: str) -> None:
        if need in self.needs:
            self.needs.remove(need)

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    preferred_time: Optional[str] = None
    recurrence: Optional[str] = None

    def is_recurring(self) -> bool:
        return bool(self.recurrence)

    def fits_in(self, minutes_available: int) -> bool:
        return self.duration_minutes <= minutes_available

@dataclass
class ScheduleItem:
    task: Task
    start_minute: Optional[int] = None
    end_minute: Optional[int] = None

    def duration(self) -> int:
        return self.task.duration_minutes

class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def validate_tasks(self, tasks: List[Task]) -> List[str]:
        errors = []
        for t in tasks:
            if t.duration_minutes <= 0:
                errors.append(f"Task '{t.title}' has non-positive duration.")
        return errors

    def generate_daily_schedule(self, owner: Owner, pet: Pet, tasks: List[Task]) -> Tuple[List[ScheduleItem], List[str]]:
        # TODO: implement greedy scheduler (sort by priority, pack until time exhausted)
        scheduled: List[ScheduleItem] = []
        explanations: List[str] = []
        return scheduled, explanations