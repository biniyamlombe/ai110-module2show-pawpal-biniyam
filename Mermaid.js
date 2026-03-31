// ...existing code...
const mermaidDiagram = `
classDiagram
    class Owner {
        +str name
        +int available_minutes
        +dict preferences
        +update_availability(minutes)
        +set_preference(key, value)
    }

    class Pet {
        +str name
        +str species
        +list needs
        +add_need(need)
        +remove_need(need)
    }

    class Task {
        +str title
        +int duration_minutes
        +str priority
        +str preferred_time
        +str recurrence
        +is_recurring()
        +fits_in(minutes_available)
    }

    class ScheduleItem {
        +Task task
        +int start_minute
        +int end_minute
        +duration()
        +overlaps(other)
    }

    class Scheduler {
        +PRIORITY_ORDER
        +validate_tasks(tasks)
        +generate_daily_schedule(owner, pet, tasks) -> (List[ScheduleItem], List[str])
    }

    Owner "1" --o "*" Pet : owns
    Owner "1" --o "*" Task : has_tasks
    Scheduler ..> Task : uses
    Scheduler ..> Pet : considers
    Scheduler ..> Owner : considers
    Scheduler "1" --o "*" ScheduleItem : produces
`;
module.exports = mermaidDiagram;