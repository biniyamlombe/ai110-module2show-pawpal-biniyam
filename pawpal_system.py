from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Collect every task for every pet owned."""
        all_tasks: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    def get_all_tasks(self, owner: Owner) -> List[tuple[Pet, Task]]:
        """Retrieve every pet task managed by an owner."""
        return owner.get_all_tasks()

    def sort_by_time(self, tasks: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Return pet tasks sorted by time in HH:MM order."""
        return sorted(tasks, key=lambda item: item[1].time)

    def filter_by_status(
        self, owner: Owner, completed: bool
    ) -> List[tuple[Pet, Task]]:
        """Return tasks filtered by completion status."""
        return [
            (pet, task)
            for pet, task in self.get_all_tasks(owner)
            if task.completed is completed
        ]

    def filter_by_pet(self, owner: Owner, pet_name: str) -> List[tuple[Pet, Task]]:
        """Return tasks for one pet name, ignoring case."""
        return [
            (pet, task)
            for pet, task in self.get_all_tasks(owner)
            if pet.name.lower() == pet_name.lower()
        ]

    def get_todays_schedule(self, owner: Owner) -> List[tuple[Pet, Task]]:
        """Return all owner tasks sorted by scheduled time."""
        tasks = self.get_all_tasks(owner)
        return self.sort_by_time(tasks)

    def detect_conflicts(self, owner: Owner) -> List[str]:
        """Return warning messages for tasks that share an exact date and time."""
        tasks_by_slot: dict[tuple[date, str], List[tuple[Pet, Task]]] = {}

        for pet, task in self.get_all_tasks(owner):
            slot = (task.due_date, task.time)
            tasks_by_slot.setdefault(slot, []).append((pet, task))

        warnings: List[str] = []
        for (due_date, time), slot_tasks in tasks_by_slot.items():
            if len(slot_tasks) > 1:
                task_labels = ", ".join(
                    f"{pet.name}: {task.description}" for pet, task in slot_tasks
                )
                warnings.append(
                    f"Conflict on {due_date.isoformat()} at {time}: {task_labels}"
                )

        return warnings

    def create_next_recurring_task(self, task: Task) -> Task | None:
        """Create the next task instance for daily or weekly recurrence."""
        frequency = task.frequency.lower()

        if frequency == "daily":
            next_due_date = task.due_date + timedelta(days=1)
        elif frequency == "weekly":
            next_due_date = task.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            due_date=next_due_date,
        )

    def mark_task_complete(self, pet: Pet, task: Task) -> Task | None:
        """Mark a task complete and create the next recurring occurrence."""
        task.mark_complete()
        next_task = self.create_next_recurring_task(task)

        if next_task is not None:
            pet.add_task(next_task)

        return next_task
