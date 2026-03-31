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
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
