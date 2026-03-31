// ...existing code...
const mermaidDiagram = `
classDiagram
    class Owner {
        +str name
        +List~Pet~ pets
        +add_pet(pet)
        +get_all_tasks()
    }

    class Pet {
        +str name
        +str species
        +int age
        +List~Task~ tasks
        +add_task(task)
        +get_tasks()
    }

    class Task {
        +str description
        +str time
        +str frequency
        +date due_date
        +bool completed
        +mark_complete()
    }

    class Scheduler {
        +get_all_tasks(owner)
        +sort_by_time(tasks)
        +filter_by_status(owner, completed)
        +filter_by_pet(owner, pet_name)
        +get_todays_schedule(owner)
        +detect_conflicts(owner)
        +create_next_recurring_task(task)
        +mark_task_complete(pet, task)
    }

    Owner "1" --o "*" Pet : owns
    Pet "1" --o "*" Task : manages
    Scheduler ..> Owner : queries
    Scheduler ..> Pet : updates
    Scheduler ..> Task : sorts and completes
`;
module.exports = mermaidDiagram;
