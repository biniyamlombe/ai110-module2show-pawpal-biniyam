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
  - Owner: holds owner information and constraints (name, available_minutes). Responsible for providing available time and preferences.
  - Pet: holds pet details (name, species, preferences). Responsible for providing pet-specific constraints (e.g., needs medication, walks).
  - Task: represents a single pet-care activity (title, duration_minutes, priority, optional preferred_time or recurrence). Responsible for describing an actionable unit to schedule.
  - Scheduler: encapsulates scheduling logic and constraints evaluation (generate_daily_schedule(owner, pet, tasks)). Responsible for selecting and ordering tasks given constraints and producing human-readable explanations.

- Responsibilities rationale:
  - Keep data containers (Owner, Pet, Task) simple as dataclasses for testability.
  - Put all decision logic in Scheduler to separate UI from algorithmic concerns.
  - UI (Streamlit app) collects inputs and displays results but does not perform scheduling decisions.

**b. Design changes**

- Did your design change during implementation?
    - Initially I considered embedding scheduling helpers directly in the UI module, but I refactored into a dedicated Scheduler class/module. Reason: improved testability, clearer separation of concerns, and easier local unit testing without the UI.
- If yes, describe at least one change and why you made it.
    - If time windows or recurring tasks are added, Task will gain start/end window attributes and Scheduler will need a timeline builder component.
- Additional changes made during implementation:
    - Moved scheduling logic out of app UI into pawpal_system.py (Scheduler class) for separation of concerns and easier testing.
    - Added an Owner.start_minute attribute so generated start_minute/end_minute map to a real point in the owner's day (default 0). This makes it easier to present schedule items as clock times later.
    - Added validation in Scheduler.validate_tasks to catch non-positive durations and unknown priority values (high|medium|low) early.
    - Created a small demo script (pawpal_demo.py) to run the scheduler locally without committing tests. Tests were written initially for local verification but not pushed per preference.
    - Converted the Mermaid content into a .mmd/.js safe export (Mermaid.js now exports a template string or saved as pawpal_diagram.mmd) to remove syntax errors.
    - Added a minimal __init__.py to the repo root to make pawpal_system import paths simpler.

**c. Main objects (building blocks)**

- Owner
  - Attributes: name (str), available_minutes (int), preferences (dict, optional)
  - Methods: update_availability(minutes), set_preference(key, value)
  - Responsibility: represent the human user and time constraints.

- Pet
  - Attributes: name (str), species (str), needs (list[str] or dict)
  - Methods: add_need(need), remove_need(need)
  - Responsibility: hold pet-specific constraints (medication, walks, feeding).

- Task
  - Attributes: title (str), duration_minutes (int), priority (str: high|medium|low), preferred_time (optional), recurrence (optional)
  - Methods: is_recurring(), fits_in(minutes_available)
  - Responsibility: describe a schedulable unit of work.

- Scheduler
  - Attributes: none (stateless functions) or config (e.g., priority_weights)
  - Methods: generate_daily_schedule(owner, pet, tasks) -> schedule, explain; validate_tasks(tasks)
  - Responsibility: encapsulate scheduling decisions, honor constraints, and produce explanations.

- (Optional) ScheduleItem / Timeline
  - Attributes: task_ref, start_minute, end_minute
  - Methods: duration(), overlaps(other)
  - Responsibility: represent placed tasks on a timeline when producing start times.
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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
