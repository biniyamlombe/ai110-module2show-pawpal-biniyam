import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Morning walk", "08:00", "Daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog", 4)
    task = Task("Dinner", "18:00", "Daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1
