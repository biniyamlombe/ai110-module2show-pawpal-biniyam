from pawpal_system import Owner, Pet, Scheduler, Task


def print_task_list(title: str, tasks: list[tuple[Pet, Task]]) -> None:
    print(title)
    print("-" * 40)

    for pet, task in tasks:
        status = "Done" if task.completed else "Not Done"
        print(
            f"{task.time} | {pet.name} ({pet.species}) | "
            f"{task.description} | {task.frequency} | {status}"
        )
    print()


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "dog", 4)
    luna = Pet("Luna", "cat", 2)

    mochi.add_task(Task("Dinner", "18:00", "Daily"))
    mochi.add_task(Task("Morning walk", "08:00", "Daily"))
    luna.add_task(Task("Play session", "12:00", "Weekly"))
    luna.add_task(Task("Feed breakfast", "07:30", "Daily"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()

    mochi.tasks[0].mark_complete()

    print_task_list("Today's Schedule", scheduler.get_todays_schedule(owner))
    print_task_list(
        "Tasks For Mochi",
        scheduler.sort_by_time(scheduler.filter_by_pet(owner, "Mochi")),
    )
    print_task_list(
        "Completed Tasks",
        scheduler.sort_by_time(scheduler.filter_by_status(owner, True)),
    )
    print_task_list(
        "Incomplete Tasks",
        scheduler.sort_by_time(scheduler.filter_by_status(owner, False)),
    )


if __name__ == "__main__":
    main()
