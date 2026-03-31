# PawPal+ Project Reflection

## 1. System Design

**Core Actions**
Based on the scenario, the three core actions a user should be able to perform are:
1. Add owner and pet information (including constraints like available time).
2. Add, view, or manage specific pet care tasks with duration and priority.
3. Generate and view a daily schedule that intelligently prioritizes and orders tasks based on available time.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- UML summary (high level):
  - Owner: represents the pet owner and stores the list of pets in the system.
  - Pet: represents one pet and stores its basic details plus its assigned tasks.
  - Task: represents one care activity with a description, time, recurrence frequency, due date, and completion state.
  - Scheduler: contains the scheduling logic for sorting, filtering, conflict detection, and recurring-task creation.

- Responsibilities rationale:
  - Keep data containers (Owner, Pet, Task) simple as dataclasses for testability.
  - Put all decision logic in Scheduler to separate UI from algorithmic concerns.
  - UI (Streamlit app) collects inputs and displays results but does not perform scheduling decisions.

**b. Design changes**

- Did your design change during implementation?
    - Initially I considered embedding scheduling helpers directly in the UI module, but I refactored into a dedicated Scheduler class/module. Reason: improved testability, clearer separation of concerns, and easier local unit testing without the UI.
- If yes, describe at least one change and why you made it.
    - One major change was simplifying the model from an earlier duration-and-priority idea into a time-based task model that fit the actual assignment more closely. This made it easier to implement sorting, recurrence, and conflict warnings clearly.
- Additional changes made during implementation:
    - Moved scheduling logic out of app UI into pawpal_system.py (Scheduler class) for separation of concerns and easier testing.
    - Added due dates to tasks so recurring daily and weekly tasks could generate the next occurrence automatically.
    - Added filtering and conflict detection methods to the Scheduler to make the app more useful and testable.
    - Connected the Streamlit UI to `st.session_state` so Owner and Scheduler objects persist across reruns.
    - Updated the UML and exported a final diagram image to match the finished backend design.

**c. Main objects (building blocks)**

- Owner
  - Attributes: name (str), pets (list[Pet])
  - Methods: add_pet(pet), get_all_tasks()
  - Responsibility: represent the human user and gather tasks across all pets.

- Pet
  - Attributes: name (str), species (str), age (int), tasks (list[Task])
  - Methods: add_task(task), get_tasks()
  - Responsibility: hold pet details and manage that pet's tasks.

- Task
  - Attributes: description (str), time (str), frequency (str), due_date (date), completed (bool)
  - Methods: mark_complete()
  - Responsibility: describe a schedulable unit of pet care.

- Scheduler
  - Attributes: none (stateless functions) or config (e.g., priority_weights)
  - Methods: get_all_tasks(owner), sort_by_time(tasks), filter_by_status(owner, completed), filter_by_pet(owner, pet_name), get_todays_schedule(owner), detect_conflicts(owner), create_next_recurring_task(task), mark_task_complete(pet, task)
  - Responsibility: encapsulate scheduling decisions, recurrence handling, sorting, filtering, and conflict warnings.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
- My scheduler currently considers task time, completion status, pet name, recurrence frequency, and exact same-time conflicts.
- I treated time and recurrence as the most important constraints because they directly affect the daily schedule and are easy for a pet owner to understand in the app and CLI demo.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- One tradeoff is that conflict detection only checks for exact matches on date and time instead of trying to detect overlapping time ranges.
- This is reasonable for the current PawPal+ version because tasks only store a single time value, not full start and end durations, so exact-match warnings stay simple, readable, and reliable for a beginner-friendly scheduler.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
- I used AI throughout the project for design planning, code generation, debugging, test creation, UI integration, and documentation cleanup.
- The most helpful prompts were specific implementation questions such as how the Scheduler should retrieve tasks from an Owner, how to sort task objects by `"HH:MM"` time strings, and how to use `timedelta` to generate the next recurring task date.
- VS Code Copilot-style workflows were especially useful when I treated AI as a coding partner for one step at a time instead of asking for the whole project at once.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
- One important example was when earlier design ideas still referred to durations, priorities, and schedule items that no longer matched the assignment's simpler task model. I chose not to keep those older ideas because they would have made the code and UML inconsistent with the actual implementation.
- I verified AI suggestions by comparing them to the assignment requirements, running `python3 -m py_compile`, running `./.venv/bin/python -m pytest`, and checking the CLI and Streamlit outputs to make sure the behavior was correct.
- Using separate chat sessions for different phases helped me stay organized because each phase had a clear goal: backend structure, UI integration, algorithmic features, testing, and final documentation.
- The biggest lesson was that I had to act as the lead architect by deciding what to keep, what to simplify, and what to reject so the final system stayed coherent.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
- I tested task completion, task addition, chronological sorting, daily recurring-task creation, and exact-time conflict detection.
- These tests were important because they covered the main behaviors that make the scheduler useful and "smart" instead of just storing plain data.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
- I am reasonably confident in the scheduler because the automated test suite passes and the CLI and Streamlit demos both show the expected behavior for sorting, recurrence, and conflicts.
- My confidence level is 4 out of 5 because the project now has automated tests for the core logic, but it still uses a lightweight scheduler model.
- If I had more time, I would test pets with no tasks, weekly recurrence creation, case-insensitive pet filtering in more detail, invalid time strings, and more complex overlapping-time scenarios.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
- I am most satisfied with the separation between the Streamlit UI and the `Scheduler` logic because it made the project easier to debug, test, and explain.
- I am also happy that the final app reflects the smart backend features instead of leaving them hidden in the Python classes.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- In another iteration, I would redesign time handling to use real datetime values throughout the system instead of storing time as strings.
- I would also improve the UI with forms, validation, and richer conflict explanations so the app feels more polished for real users.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
- My biggest takeaway is that powerful AI tools are most helpful when I use them as structured collaborators, not as decision-makers. The best results came from breaking the project into phases, asking focused questions, and then using human judgment to keep the system simple, consistent, and aligned with the assignment goals.
