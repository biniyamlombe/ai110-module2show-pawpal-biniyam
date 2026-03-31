from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    frequency: str
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

    def mark_task_complete(self, task: Task) -> None:
        """Mark a scheduled task as complete."""
        task.mark_complete()
