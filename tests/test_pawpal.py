import sys
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Morning walk", "08:00", "Daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog", 4)
    task = Task("Dinner", "18:00", "Daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_get_todays_schedule_sorts_tasks_in_chronological_order() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 4)
    scheduler = Scheduler()

    pet.add_task(Task("Dinner", "18:00", "Daily"))
    pet.add_task(Task("Morning walk", "08:00", "Daily"))
    pet.add_task(Task("Lunch", "12:00", "Daily"))
    owner.add_pet(pet)

    schedule = scheduler.get_todays_schedule(owner)

    assert [task.time for _, task in schedule] == ["08:00", "12:00", "18:00"]


def test_mark_task_complete_creates_next_daily_task() -> None:
    pet = Pet("Mochi", "dog", 4)
    scheduler = Scheduler()
    task = Task("Dinner", "18:00", "Daily", due_date=date(2026, 3, 31))
    pet.add_task(task)

    next_task = scheduler.mark_task_complete(pet, task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.description == "Dinner"
    assert next_task.time == "18:00"
    assert next_task.frequency == "Daily"
    assert next_task.due_date == date(2026, 4, 1)
    assert next_task.completed is False
    assert len(pet.tasks) == 2


def test_detect_conflicts_flags_duplicate_task_times() -> None:
    owner = Owner("Jordan")
    scheduler = Scheduler()
    mochi = Pet("Mochi", "dog", 4)
    luna = Pet("Luna", "cat", 2)

    mochi.add_task(Task("Morning walk", "08:00", "Daily", due_date=date(2026, 3, 31)))
    luna.add_task(Task("Take medication", "08:00", "Daily", due_date=date(2026, 3, 31)))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Conflict on 2026-03-31 at 08:00" in warnings[0]
    assert "Mochi: Morning walk" in warnings[0]
    assert "Luna: Take medication" in warnings[0]


def test_find_next_available_slot_returns_next_open_time() -> None:
    owner = Owner("Jordan")
    scheduler = Scheduler()
    mochi = Pet("Mochi", "dog", 4)

    mochi.add_task(Task("Breakfast", "08:00", "Daily", due_date=date(2026, 3, 31)))
    mochi.add_task(Task("Walk", "08:30", "Daily", due_date=date(2026, 3, 31)))
    owner.add_pet(mochi)

    next_slot = scheduler.find_next_available_slot(
        owner,
        due_date=date(2026, 3, 31),
        preferred_time="08:00",
        interval_minutes=30,
        end_time="10:00",
    )

    assert next_slot == "09:00"
