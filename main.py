from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(owner: Owner, scheduler: Scheduler) -> None:
    print("Today's Schedule")
    print("-" * 40)

    for pet, task in scheduler.get_todays_schedule(owner):
        status = "Done" if task.completed else "Not Done"
        print(
            f"{task.time} | {pet.name} ({pet.species}) | "
            f"{task.description} | {task.frequency} | {status}"
        )


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "dog", 4)
    luna = Pet("Luna", "cat", 2)

    mochi.add_task(Task("Morning walk", "08:00", "Daily"))
    mochi.add_task(Task("Dinner", "18:00", "Daily"))
    luna.add_task(Task("Feed breakfast", "07:30", "Daily"))
    luna.add_task(Task("Play session", "12:00", "Weekly"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()
    print_schedule(owner, scheduler)


if __name__ == "__main__":
    main()
