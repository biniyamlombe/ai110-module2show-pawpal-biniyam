import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler


def build_task_rows(tasks: list[tuple[Pet, Task]]) -> list[dict[str, str | bool]]:
    rows: list[dict[str, str | bool]] = []
    for pet, task in tasks:
        rows.append(
            {
                "due date": task.due_date.isoformat(),
                "time": task.time,
                "pet": pet.name,
                "species": pet.species,
                "task": task.description,
                "frequency": task.frequency,
                "completed": task.completed,
            }
        )
    return rows

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

st.markdown("### Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=50, value=2)

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species, int(age)))
    st.success(f"{pet_name} was added for {owner.name}.")

if owner.pets:
    st.write("Current pets:")
    pet_rows = [{"name": pet.name, "species": pet.species, "age": pet.age} for pet in owner.pets]
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add a Task")
st.caption("Tasks are stored on the selected pet and kept in session state.")

if owner.pets:
    pet_options = {f"{pet.name} ({pet.species})": pet for pet in owner.pets}
    selected_pet_label = st.selectbox("Choose a pet", list(pet_options.keys()))
    selected_pet = pet_options[selected_pet_label]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task description", value="Morning walk")
    with col2:
        task_time = st.text_input("Time", value="08:00")
    with col3:
        task_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "As needed"])

    if st.button("Add task"):
        selected_pet.add_task(Task(task_description, task_time, task_frequency))
        st.success(f"Added '{task_description}' for {selected_pet.name}.")

    task_rows = build_task_rows(scheduler.get_todays_schedule(owner))

    if task_rows:
        st.write("Current tasks:")
        st.table(task_rows)
    else:
        st.info("No tasks yet. Add one above.")

    all_pet_tasks = []
    for pet in owner.pets:
        for task in pet.get_tasks():
            all_pet_tasks.append((pet, task))

    if all_pet_tasks:
        st.markdown("### Update a Task")
        incomplete_tasks = [
            (pet, task) for pet, task in all_pet_tasks if not task.completed
        ]

        if incomplete_tasks:
            completion_options = {
                f"{task.time} | {pet.name} | {task.description}": (pet, task)
                for pet, task in incomplete_tasks
            }
            selected_task_label = st.selectbox(
                "Choose a task to mark complete",
                list(completion_options.keys()),
            )

            if st.button("Mark selected task complete"):
                selected_task_pet, selected_task = completion_options[selected_task_label]
                next_task = scheduler.mark_task_complete(selected_task_pet, selected_task)
                st.success(f"Marked '{selected_task.description}' as complete.")
                if next_task is not None:
                    st.info(
                        f"Created next recurring task for {selected_task_pet.name} on "
                        f"{next_task.due_date.isoformat()} at {next_task.time}."
                    )
        else:
            st.success("All current tasks are already marked complete.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Schedule Overview")
st.caption("View the smart schedule with sorting, filtering, and conflict warnings.")

all_tasks = scheduler.get_todays_schedule(owner)

if all_tasks:
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        st.warning("Scheduling conflicts detected:")
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No task conflicts detected.")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        pet_filter = st.selectbox(
            "Filter by pet",
            ["All pets"] + [pet.name for pet in owner.pets],
        )
    with filter_col2:
        status_filter = st.selectbox(
            "Filter by status",
            ["All tasks", "Incomplete only", "Completed only"],
        )

    filtered_tasks = all_tasks
    if pet_filter != "All pets":
        filtered_tasks = scheduler.sort_by_time(
            scheduler.filter_by_pet(owner, pet_filter)
        )

    if status_filter == "Incomplete only":
        filtered_tasks = [
            (pet, task) for pet, task in filtered_tasks if task.completed is False
        ]
    elif status_filter == "Completed only":
        filtered_tasks = [
            (pet, task) for pet, task in filtered_tasks if task.completed is True
        ]

    if filtered_tasks:
        st.write("Today's Schedule:")
        st.table(build_task_rows(filtered_tasks))
    else:
        st.info("No tasks match the selected filters.")
else:
    st.warning("Add at least one pet and one task to see the schedule.")
