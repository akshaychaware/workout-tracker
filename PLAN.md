# Training Tracker — Project Plan

## 1. Project Overview

### Project Name

**Training Tracker**

### Purpose

Build a simple application to track the daily training and exercise routine of a Greyhound being prepared for racing.

The application should make it easy to:

- Define the dog's weekly training routine.
- See what training is planned for today.
- Record what actually happened.
- Mark training as completed, skipped, or partially completed.
- Record simple observations or notes.
- Review the dog's training history.
- Track consistency over time.

The first version should remain intentionally simple. The goal is not to build a professional veterinary, fitness, or race-performance platform immediately. We will first solve the basic problem of maintaining a reliable daily training record.

---

# 2. Core Problem

The training currently follows a simple routine such as:

- Monday → Running
- Tuesday → Walking
- Wednesday → Swimming for 20 minutes
- Thursday → Rest
- Friday → Running
- Saturday → Walking
- Sunday → Rest

The problem this application solves is remembering and recording:

1. What was planned?
2. What was actually done?
3. Was the session completed?
4. If it was not completed, why?
5. What observations were made?

The application should turn the weekly routine into a historical record that can be reviewed later.

---

# 3. Product Vision

The long-term vision is to have a lightweight training journal for the Greyhound.

The application should eventually answer questions such as:

- What was today's training?
- What training is planned this week?
- How consistently has the dog been trained?
- How many running sessions were completed?
- How many swimming sessions were completed?
- How long were the swimming sessions?
- Which training sessions were skipped?
- What notes were recorded on a particular day?
- How has the training routine changed over time?

Future features may include race preparation, performance metrics, training load, charts, reminders, and more advanced tracking.

Those features are intentionally outside the first version unless they become necessary.

---

# 4. Initial Scope — V1

V1 will focus on four core concepts.

## 4.1 Dog

The application should maintain basic information about the dog.

Initial information:

- Name
- Breed
- Age or date of birth
- Optional weight
- Optional notes

Example:

```text
Name: Luna
Breed: Greyhound
```

The application should be designed so that additional dogs could be supported later, even if V1 primarily uses one dog.

---

## 4.2 Exercise Types

The application should have a list of available training/activity types.

Initial exercise types:

- Running
- Walking
- Swimming
- Hill Climbing
- Rest

More activities can be added later.

Each exercise type may eventually have its own relevant measurements.

Examples:

### Running

Possible measurements:

- Duration
- Distance
- Number of runs
- Notes

### Walking

Possible measurements:

- Duration
- Distance
- Notes

### Swimming

Possible measurements:

- Duration

Example:

```text
Swimming
Planned Duration: 20 minutes
```

### Hill Climbing

Possible measurements:

- Duration
- Number of repetitions
- Notes

### Rest

No physical activity is required.

Rest is still part of the training plan because recovery is intentionally scheduled.

---

# 5. Weekly Training Plan

The application should allow a weekly routine to be configured.

Example:

```text
Monday     → Running
Tuesday    → Walking
Wednesday  → Swimming — 20 minutes
Thursday   → Rest
Friday     → Running
Saturday   → Walking
Sunday     → Rest
```

The schedule should not be hard-coded into the application.

The user should be able to change the schedule.

For example:

```text
Wednesday
Swimming — 20 minutes
```

can later become:

```text
Wednesday
Swimming — 30 minutes
```

without requiring a code change.

---

# 6. Planned vs Actual Training

This is one of the most important concepts in the application.

The application should distinguish between:

### Planned

What the weekly training plan says should happen.

Example:

```text
Wednesday

Swimming
20 minutes
```

### Actual

What actually happened.

Example:

```text
Wednesday

Swimming
Planned: 20 minutes
Actual: 18 minutes

Status: Completed
```

Another example:

```text
Wednesday

Swimming
Planned: 20 minutes
Actual: 0 minutes

Status: Skipped

Reason:
Dog appeared tired.
```

This distinction should remain part of the design from the beginning.

---

# 7. Daily Training Record

Every planned training day should be capable of producing a daily record.

A daily record should contain information such as:

```text
Date
Dog
Exercise
Planned values
Actual values
Status
Notes
```

Initial status values:

- Planned
- Completed
- Partially Completed
- Skipped

Rest days can be recorded as:

```text
Status: Rest
```

or represented as a completed planned rest day, depending on the final domain design.

---

# 8. Daily User Workflow

The primary workflow should be extremely simple.

## Step 1 — Open the application

The user sees today's training.

Example:

```text
Today — Wednesday

Swimming
Planned: 20 minutes
```

## Step 2 — Perform the training

The user takes the dog through the planned activity.

## Step 3 — Record the result

Example:

```text
Planned: 20 minutes
Actual: 18 minutes
Status: Completed
```

## Step 4 — Add optional notes

Example:

```text
Good session.
Dog was energetic.
```

## Step 5 — Save

The session becomes part of the dog's permanent training history.

---

# 9. Main Application Screens — V1

The initial application should have a small number of screens.

## 9.1 Dashboard

Purpose:

Show the current day's training and a quick view of the week.

Example:

```text
DOG TRAINING

Luna

TODAY

Swimming
Planned: 20 min

[Complete Training]


THIS WEEK

Mon  Running       ✓
Tue  Walking       ✓
Wed  Swimming      ○
Thu  Rest          -
Fri  Running       ○
Sat  Walking       ○
Sun  Rest          -
```

The dashboard should answer:

> What do I need to do today?

---

## 9.2 Training Plan

Purpose:

View and modify the weekly routine.

Example:

```text
Weekly Training Plan

Monday
Running

Tuesday
Walking

Wednesday
Swimming — 20 min

Thursday
Rest

Friday
Running

Saturday
Walking

Sunday
Rest
```

---

## 9.3 Daily Training Entry

Purpose:

Record the actual training.

Example:

```text
Swimming

Date:
29 Sep 2026

Planned:
20 minutes

Actual:
18 minutes

Status:
Completed

Notes:
Good session.
```

---

## 9.4 History

Purpose:

Review previous training records.

Example:

```text
Training History

29 Sep
Swimming
18 min / 20 min
Completed

28 Sep
Rest
Completed

27 Sep
Walking
30 min
Completed
```

Filtering can be added later.

---

# 10. Training History

The application should retain historical records.

A training record should not be overwritten simply because the weekly schedule changes.

Example:

September 1:

```text
Swimming
20 minutes
```

Later the weekly plan changes to:

```text
Swimming
30 minutes
```

The September 1 record must still show:

```text
Planned: 20 minutes
Actual: 20 minutes
```

Historical records represent what was planned and performed at that time.

---

# 11. Basic Statistics — V1

V1 can provide simple statistics.

Examples:

### Weekly

```text
Training Days: 5
Completed: 4
Skipped: 1
Rest Days: 2
```

### Exercise count

```text
Running: 2
Walking: 2
Swimming: 1
```

### Swimming

```text
Sessions: 4
Total Time: 78 minutes
Average: 19.5 minutes
```

The statistics should be descriptive rather than trying to automatically judge the dog's fitness.

---

# 12. What V1 Will NOT Do

To keep the first version focused, V1 will not initially include:

- Medical diagnosis
- Veterinary recommendations
- Automatic health assessment
- Automatic training prescriptions
- AI-generated training plans
- GPS tracking
- Live heart-rate monitoring
- Wearable integration
- Complex performance analytics
- Race prediction
- Automatic injury detection
- Advanced nutrition management
- Multi-user permissions
- Social features

These can be considered later if there is a genuine need.

---

# 13. Future Scope

After V1 is stable, possible future versions may include:

## V2 — Better Training Metrics

- Distance
- Speed
- Pace
- Repetitions
- Track/surface
- Training intensity
- More detailed session measurements

## V3 — Training Analytics

- Weekly volume
- Monthly volume
- Exercise distribution
- Training consistency
- Performance trends
- Personal records
- Charts

## V4 — Race Preparation

Introduce race-specific concepts:

```text
Race
  ↓
Race Distance
  ↓
Target Date
  ↓
Training Program
  ↓
Training Phases
  ↓
Daily Sessions
```

Possible phases may include:

- Conditioning
- Strength
- Speed
- Race preparation
- Taper
- Recovery

The exact training methodology should be based on the actual training program rather than assumptions made by the software.

## V5 — Advanced Tracking

Potential future features:

- GPS running tracking
- Wearable/device integration
- Heart-rate data
- Recovery measurements
- Training load
- Notifications
- Calendar integration
- Multiple dogs
- Multiple training programs

---

# 14. Product Principles

The project should follow these principles.

## 14.1 Keep it simple

The user should be able to record a training session in seconds.

The application should not turn a simple activity such as swimming for 20 minutes into a complicated data-entry process.

## 14.2 Record reality

The application should distinguish:

```text
What was planned
        vs
What actually happened
```

## 14.3 Preserve history

Historical records should remain accurate even when future training plans change.

## 14.4 Start small

Do not build future functionality before the core workflow is working.

## 14.5 Make the data useful

Every field should have a reason to exist.

Avoid collecting information simply because it might be useful someday.

---

# 15. Core Use Cases

The initial system should support these use cases.

### UC-01 — Create Dog

Create the dog profile.

### UC-02 — Configure Weekly Training Plan

Assign an activity to each day of the week.

### UC-03 — View Today's Training

See what activity is planned today.

### UC-04 — Record Training

Record what actually happened.

### UC-05 — Mark Training Status

Mark a session as:

- Completed
- Partially Completed
- Skipped

### UC-06 — Add Training Notes

Record simple observations.

### UC-07 — View Training History

Review previous sessions.

### UC-08 — View Basic Statistics

View simple weekly/monthly training summaries.

These use cases define the initial product boundary.

---

# 16. Initial Domain Model

The first domain model will likely contain:

```text
Dog
  │
  ├── Training Plan
  │       │
  │       └── Planned Training
  │
  └── Training Records
          │
          └── Actual Training
```

Possible entities:

```text
Dog
ExerciseType
TrainingPlan
TrainingPlanDay
TrainingSession
```

The final database model should be designed only after the use cases are reviewed.

---

# 17. Development Approach

Development should happen incrementally.

We should avoid implementing the entire application at once.

Recommended order:

```text
1. Define requirements
        ↓
2. Define use cases
        ↓
3. Define domain model
        ↓
4. Define database model
        ↓
5. Build backend foundation
        ↓
6. Build training plan
        ↓
7. Build daily training records
        ↓
8. Build dashboard
        ↓
9. Build history
        ↓
10. Add basic statistics
        ↓
11. Test complete workflow
        ↓
12. Release V1
```

Each stage should be completed and verified before moving to the next major stage.

---

# 18. Definition of Done — V1

V1 is considered complete when the user can:

- Create a dog.
- Define a weekly training schedule.
- View today's planned training.
- Record a completed training session.
- Record a partially completed session.
- Record a skipped session.
- Record actual duration where applicable.
- Add notes.
- View previous training records.
- View the current week's training status.
- View basic training statistics.
- Change the future weekly schedule without corrupting historical records.

The complete workflow should work from beginning to end without requiring manual database changes.

---

# 19. Development Tracking

This section should be updated as development progresses.

## Phase 1 — Requirements

- [ ] Define actual real-world training workflow
- [ ] Confirm initial exercise types
- [ ] Confirm weekly schedule behavior
- [ ] Define training session statuses
- [ ] Define minimum information required for each activity
- [ ] Confirm V1 scope

## Phase 2 — Domain Design

- [ ] Define entities
- [ ] Define relationships
- [ ] Define domain rules
- [ ] Define historical data behavior
- [ ] Review domain model

## Phase 3 — Database Design

- [ ] Design tables
- [ ] Define primary keys
- [ ] Define foreign keys
- [ ] Define indexes
- [ ] Define constraints
- [ ] Create initial migration

## Phase 4 — Backend

- [ ] Project setup
- [ ] Dog APIs
- [ ] Exercise type APIs
- [ ] Training plan APIs
- [ ] Training session APIs
- [ ] History APIs
- [ ] Statistics APIs
- [ ] Backend tests

## Phase 5 — Frontend

- [ ] Project setup
- [ ] Dashboard
- [ ] Training plan screen
- [ ] Daily training screen
- [ ] History screen
- [ ] Basic statistics
- [ ] Frontend validation

## Phase 6 — Integration

- [ ] Connect frontend and backend
- [ ] Test complete daily workflow
- [ ] Test schedule changes
- [ ] Test historical records
- [ ] Test edge cases
- [ ] Fix integration issues

## Phase 7 — V1 Completion

- [ ] End-to-end testing
- [ ] Clean up code
- [ ] Documentation
- [ ] Deployment
- [ ] V1 release

---

# 20. Important Design Decisions

Decisions should be recorded here as the project evolves.

| Decision | Status | Notes |
|---|---|---|
| V1 focuses on simple daily training tracking | Confirmed | Avoid unnecessary complexity |
| Planned and actual training are separate concepts | Confirmed | Important for historical accuracy |
| Weekly schedule should be configurable | Confirmed | Do not hard-code routine |
| Rest is part of the training schedule | Confirmed | Recovery is intentionally planned |
| Historical records must not change when future plans change | Confirmed | Preserve historical truth |
| Advanced analytics are deferred | Confirmed | Consider after V1 |

---

# 21. Open Questions

These should be answered before finalizing the domain/database design.

- [ ] What exact weekly routine should be the initial default?
- [ ] Should one day support multiple activities?
- [ ] Should an activity have a planned duration?
- [ ] Which activities need distance?
- [ ] Which activities need repetitions?
- [ ] Should the user record intensity?
- [ ] Should the user record the dog's condition before/after training?
- [ ] Should weight be tracked?
- [ ] Should the application support more than one dog?
- [ ] Should training plans have start/end dates?
- [ ] How should a skipped session be explained?
- [ ] Should the application support future race dates?

These questions should be resolved only when they become necessary for the next implementation stage.

---

# 22. Project Rule

The project should remain **issue-driven**.

For each meaningful feature:

1. Define the problem.
2. Create an issue.
3. Define acceptance criteria.
4. Implement the smallest useful change.
5. Add tests.
6. Verify the feature.
7. Mark the issue complete.
8. Update this plan.
9. Move to the next issue.

Do not prematurely implement future features simply because they are listed in this document.

---

# 23. Current Status

**Project:** Training Tracker

**Version:** V1 — Initial Planning

**Status:** Requirements / Use-case discussion

**Current focus:**

> Understand the real-world training workflow before designing the technical architecture.

**Next milestone:**

> Finalize V1 use cases and domain model.

---

# 24. Change Log

## 2026-09-29

- Created initial project plan.
- Defined the project as a simple Greyhound daily training tracker.
- Established the initial concept of planned vs actual training.
- Defined initial activities:
  - Running
  - Walking
  - Swimming
  - Hill Climbing
  - Rest
- Defined configurable weekly training schedule.
- Defined basic daily training records.
- Defined initial V1 scope.
- Deferred advanced race analytics, GPS, health monitoring, AI, and wearable integrations.
