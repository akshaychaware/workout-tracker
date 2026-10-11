# Training Tracker — Architecture

## 1. Architecture Overview

Training Tracker will start as a **modular monolith**.

The application is intentionally designed to remain simple for V1 while keeping the domain model flexible enough for future training features.

The primary architecture is:

```text
                    Training Tracker
                           │
             ┌─────────────┴─────────────┐
             │                           │
        Frontend                    Backend API
             │                           │
       Web Application          Application Logic
                                         │
                                  ┌──────┴──────┐
                                  │             │
                              Database      Storage
```

The initial implementation should not use microservices.

---

# 2. Architecture Goals

The architecture should:

1. Keep the application simple.
2. Clearly separate frontend and backend responsibilities.
3. Keep business rules inside the backend.
4. Preserve historical training data.
5. Allow the weekly training plan to change without modifying old records.
6. Support multiple activities in a single day.
7. Allow new exercise/activity types to be added without redesigning the system.
8. Make future features possible without prematurely implementing them.
9. Keep V1 easy to develop, test, deploy, and maintain.

---

# 3. High-Level Architecture

```text
┌────────────────────────────────────────────────────┐
│                    Frontend                        │
│                                                    │
│  Dashboard                                        │
│  Training Plan                                    │
│  Daily Session                                    │
│  History                                          │
│  Statistics                                       │
└────────────────────────┬───────────────────────────┘
                         │
                      HTTP/JSON
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│                    Backend API                     │
│                                                    │
│  Dog Module                                       │
│  Exercise Module                                  │
│  Training Plan Module                             │
│  Training Session Module                          │
│  Statistics Module                                │
└────────────────────────┬───────────────────────────┘
                         │
                       ORM/SQL
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│                  Relational DB                     │
│                                                    │
│  dogs                                              │
│  exercise_types                                    │
│  training_plans                                    │
│  training_plan_days                                │
│  planned_activities                                │
│  training_sessions                                 │
└────────────────────────────────────────────────────┘
```

---

# 4. Architectural Style

## Modular Monolith

V1 will use a modular monolith instead of microservices.

All backend modules will run as one application.

Conceptually:

```text
Backend Application
│
├── Dog
├── Exercise
├── Training Plan
├── Training Session
└── Statistics
```

This provides separation of responsibilities without introducing distributed-system complexity.

### Why not microservices?

The current application does not require:

- Independent service scaling
- Distributed processing
- Multiple teams
- Service-to-service communication
- Multiple independently deployed services
- Distributed messaging

Introducing microservices at this stage would increase complexity without solving an existing problem.

---

# 5. Frontend

The frontend is responsible for:

- Displaying the training plan.
- Displaying today's training.
- Collecting user input.
- Displaying training history.
- Displaying statistics.
- Performing basic UI validation.
- Sending requests to the backend API.

The frontend should **not own core business rules**.

For example, the frontend should not determine:

```text
Wednesday = Swimming
```

Instead:

```text
Frontend
   │
   │ GET /api/training/today
   ▼
Backend
   │
   ├── Determine today's date
   ├── Find active plan
   ├── Find today's planned activities
   └── Return training
```

The frontend displays the backend result.

---

# 6. Backend

The backend is the source of truth for business logic.

Responsibilities include:

- Managing dogs.
- Managing exercise types.
- Managing training plans.
- Generating today's planned training.
- Recording training sessions.
- Validating session status.
- Preserving historical values.
- Retrieving training history.
- Calculating basic statistics.

The backend should expose a REST API initially.

---

# 7. Backend Module Structure

The backend should be organized around business concepts.

Conceptually:

```text
backend/
└── src/
    │
    ├── dog/
    │
    ├── exercise/
    │
    ├── training-plan/
    │
    ├── training-session/
    │
    └── statistics/
```

Each module should contain the logic required for its domain.

A module may internally contain:

```text
module/
├── controller
├── service
├── repository
├── entity/model
├── dto
└── tests
```

The exact framework-specific structure can be finalized later.

---

# 8. Domain-Oriented Modules

## Dog Module

Responsible for:

- Creating dogs.
- Updating dog information.
- Retrieving dog information.

Example:

```text
Dog
├── id
├── name
├── breed
├── date_of_birth
└── weight
```

---

## Exercise Module

Responsible for exercise/activity types.

Initial activities:

```text
Running
Walking
Swimming
Hill Climbing
Rest
```

The system should treat these as configurable activity types rather than hard-coded application logic.

Future examples could include:

```text
Sprint
Warm-up
Cool-down
Recovery Walk
Track Work
```

Adding an activity should ideally not require changes to the core training architecture.

---

## Training Plan Module

Responsible for defining planned training.

Example:

```text
Weekly Training Plan

Monday
  Running

Tuesday
  Walking

Wednesday
  Swimming — 20 minutes

Thursday
  Rest
```

The plan is configurable.

---

## Training Session Module

Responsible for recording what actually happened.

Example:

```text
Date: 29 Sep 2026
Activity: Swimming

Planned:
20 minutes

Actual:
18 minutes

Status:
Partially Completed

Notes:
Good session.
```

This module is central to the application's historical record.

---

## Statistics Module

Responsible for descriptive summaries.

Examples:

```text
Training Days: 5
Completed: 4
Skipped: 1
Rest Days: 2
```

Activity summaries:

```text
Running: 2 sessions
Walking: 2 sessions
Swimming: 1 session
```

The statistics module should initially query the training session data directly.

A separate analytics service or data warehouse is not required for V1.

---

# 9. Domain Model

The core domain relationship should look like:

```text
Dog
 │
 ├───────────────┐
 │               │
 ▼               ▼
Training Plan   Training Sessions
 │
 ▼
Plan Days
 │
 ▼
Planned Activities
 │
 ▼
Exercise Type
```

A dog can have training plans.

A training plan contains planned activities.

Training sessions represent actual training performed by the dog.

---

# 10. Supporting Multiple Activities Per Day

The domain model should support multiple activities on the same day even if the V1 UI initially uses one simple activity per day.

Example:

```text
Wednesday
│
├── Warm-up
├── Running
├── Swimming — 20 min
└── Recovery
```

Therefore, the architecture should avoid assuming:

```text
One day = one activity
```

Instead:

```text
Training Plan
     │
     └── Plan Day
            │
            ├── Activity 1
            ├── Activity 2
            └── Activity 3
```

This provides future flexibility without requiring immediate complexity in the UI.

---

# 11. Database Architecture

A relational database is appropriate for the application.

Initial conceptual tables:

```text
dogs
exercise_types
training_plans
training_plan_days
planned_activities
training_sessions
```

---

## 11.1 dogs

```text
id
name
breed
date_of_birth
weight
created_at
updated_at
```

---

## 11.2 exercise_types

```text
id
name
description
created_at
updated_at
```

Example:

```text
1 | Running
2 | Walking
3 | Swimming
4 | Hill Climbing
5 | Rest
```

---

## 11.3 training_plans

```text
id
dog_id
name
start_date
end_date
is_active
created_at
updated_at
```

A plan represents a period during which a particular training schedule is active.

---

## 11.4 training_plan_days

```text
id
training_plan_id
day_of_week
```

This represents a day within a training plan.

---

## 11.5 planned_activities

```text
id
training_plan_day_id
exercise_type_id
sequence
planned_duration
planned_distance
planned_repetitions
notes
```

Not every field will be required for every activity.

For example:

```text
Swimming
planned_duration = 20
```

while:

```text
Running
planned_distance = 5
planned_duration = 30
```

The exact activity-specific metric model should be finalized during detailed database design.

---

## 11.6 training_sessions

Conceptually:

```text
id
dog_id
planned_activity_id
exercise_type_id
date
planned_duration
actual_duration
planned_distance
actual_distance
status
notes
created_at
updated_at
```

The final fields will be refined during database design.

---

# 12. Historical Data Preservation

Historical accuracy is a major architectural requirement.

Suppose the original plan is:

```text
September

Wednesday → Swimming → 20 minutes
```

Later, the plan changes:

```text
October

Wednesday → Swimming → 30 minutes
```

The September session must remain:

```text
Planned: 20 minutes
Actual: 20 minutes
```

It must not dynamically become:

```text
Planned: 30 minutes
```

Therefore, when a training session is recorded, important planned values should be preserved as part of the session record.

Conceptually:

```text
Training Plan
      │
      │ creates planned activity
      ▼
Training Session
      │
      ├── planned values snapshot
      └── actual values
```

This allows the application to accurately reconstruct historical training.

---

# 13. Training Session Lifecycle

A session begins as planned.

```text
PLANNED
   │
   ├───────────────┐
   │               │
   ▼               ▼
COMPLETED     PARTIALLY_COMPLETED
   │               │
   └───────┬───────┘
           ▼
         SAVED
```

A session can also become:

```text
PLANNED
   │
   ▼
SKIPPED
```

The backend should validate session status values.

The frontend should not be trusted as the sole source of business validation.

---

# 14. REST API

Initial API structure:

```text
/api/dogs

/api/exercise-types

/api/training-plans

/api/training-plans/:id/days

/api/training/today

/api/training/sessions

/api/training/history

/api/statistics
```

---

## Example — Today's Training

```http
GET /api/training/today
```

Example response:

```json
{
  "date": "2026-09-29",
  "activities": [
    {
      "exercise": "Swimming",
      "plannedDuration": 20,
      "status": "PLANNED"
    }
  ]
}
```

---

## Example — Record Session

```http
POST /api/training/sessions
```

Example:

```json
{
  "plannedActivityId": 12,
  "actualDuration": 18,
  "status": "PARTIALLY_COMPLETED",
  "notes": "Good session"
}
```

The backend should determine and validate the relevant dog, plan, activity, and historical values.

---

# 15. Statistics Architecture

V1 statistics should be calculated from training sessions.

```text
Statistics API
      │
      ▼
Training Session Repository
      │
      ▼
SQL Aggregation
```

Examples:

```text
COUNT(*)
SUM(actual_duration)
AVG(actual_duration)
GROUP BY exercise_type
```

No separate analytics database is required initially.

---

# 16. Authentication and Users

The application may initially be used by a single person.

However, the architecture should leave room for user ownership.

Future conceptual model:

```text
User
 │
 └── Dogs
       │
       └── Training Plans
             │
             └── Training Sessions
```

Whether authentication is included in V1 will be decided during implementation planning.

---

# 17. Project Structure

A possible repository structure:

```text
training-tracker/
│
├── frontend/
│
├── backend/
│
├── docs/
│   ├── PLAN.md
│   ├── ARCHITECTURE.md
│   └── USER_GUIDE.md
│
├── docker-compose.yml
└── README.md
```

The exact directory structure may change according to the selected technology stack.

---

# 18. Deployment Architecture

The initial deployment should remain simple.

Conceptually:

```text
                 Internet / Local Network
                           │
                           ▼
                    Frontend Application
                           │
                           ▼
                       Backend API
                           │
                           ▼
                      PostgreSQL
```

Docker can be used to make local development and deployment consistent.

A reverse proxy can be introduced when required by the deployment environment.

---

# 19. Technology Selection

The architecture does not require a specific technology yet.

The following decisions should be made after the domain model is finalized:

- Frontend framework
- Backend framework
- Database
- ORM
- Authentication approach
- Deployment platform
- Containerization strategy

The technology should serve the domain rather than determine the domain model.

---

# 20. V1 Architecture Boundaries

V1 should contain:

```text
Frontend
    ↓
REST API
    ↓
Modular Backend
    ↓
Relational Database
```

V1 should not contain:

```text
Microservices
Message queues
Event streaming
Data warehouse
Separate analytics service
AI service
GPS processing pipeline
Wearable ingestion pipeline
```

Those can be introduced only when an actual requirement justifies them.

---

# 21. Core Architectural Principles

## 21.1 Backend is the source of truth

Business rules should live in the backend.

## 21.2 Domain-oriented modules

Organize code around concepts such as Dog, Training Plan, and Training Session.

## 21.3 Preserve history

Old training records must remain accurate when future plans change.

## 21.4 Activity-driven design

Running, walking, swimming, hill climbing, and rest are activity types.

The architecture should not be built around a fixed list of exercises.

## 21.5 Multiple activities per day

The domain should allow multiple planned activities on a single day.

## 21.6 Keep V1 simple

Do not introduce infrastructure before it solves a real problem.

---

# 22. Architecture Decision Log

| Decision | Status | Reason |
|---|---|---|
| Use a modular monolith for V1 | Confirmed | Simple and maintainable |
| Use a relational database | Proposed | Training data has clear relationships |
| Backend owns business rules | Confirmed | Single source of truth |
| Separate planned and actual training | Confirmed | Required for accurate tracking |
| Preserve planned values in historical sessions | Confirmed | Prevent historical data from changing |
| Support multiple activities per day | Confirmed | Keeps the domain flexible |
| Treat exercises as activity types | Confirmed | Allows new activities without redesign |
| Use REST API initially | Proposed | Simple frontend/backend integration |
| Avoid microservices in V1 | Confirmed | No current requirement |
| Avoid separate analytics service in V1 | Confirmed | Basic statistics can use database queries |

---

# 23. Open Architecture Questions

These should be resolved before implementation begins:

- [ ] Select frontend technology.
- [ ] Select backend technology.
- [ ] Select relational database.
- [ ] Decide ORM.
- [ ] Finalize domain entities.
- [ ] Finalize database relationships.
- [ ] Finalize activity metric strategy.
- [ ] Decide whether V1 supports multiple dogs.
- [ ] Decide whether V1 requires authentication.
- [ ] Define API conventions.
- [ ] Define error-handling conventions.
- [ ] Define testing strategy.
- [ ] Define deployment environment.

---

# 24. Architecture Status

**Project:** Training Tracker

**Version:** V1

**Architecture Status:** Initial architecture defined

**Current focus:**

> Finalize the domain model and relationships before selecting implementation technologies.

**Next step:**

> Design the detailed domain model and database relationships.


# 25. Client Applications — Web and Mobile

Training Tracker should support both **Web** and **Mobile** clients while keeping a single backend and database.

The architecture is:

```text
                         ┌───────────────┐
                         │   Angular Web │
                         └───────┬───────┘
                                 │
                         ┌───────▼───────┐
                         │ Mobile Client │
                         │ Flutter / RN  │
                         └───────┬───────┘
                                 │
                           REST / JSON
                                 │
                    ┌────────────▼────────────┐
                    │     NestJS Backend      │
                    │                         │
                    │ Dog                     │
                    │ Exercise                │
                    │ Training Plan           │
                    │ Training Session        │
                    │ Statistics              │
                    └────────────┬────────────┘
                                 │
                              TypeORM
                                 │
                    ┌────────────▼────────────┐
                    │       PostgreSQL         │
                    └─────────────────────────┘
```

## Web Application

The web application will use:

**Angular**

The web client will provide:

- Dashboard
- Training plan management
- Daily training entry
- Training history
- Statistics
- Dog management

The web application is useful for configuration, reviewing history, and managing the training plan.

---

## Mobile Application

A mobile application should be part of the overall architecture because the primary training activity happens outside the home.

The mobile application can eventually provide:

- Today's training
- Quick session recording
- Start/finish training
- Quick notes
- Training history
- Training status
- Future GPS tracking
- Future offline support
- Future device/wearable integration

The mobile technology is not finalized yet.

Candidate options:

```text
Flutter
React Native
```

The final choice will be made before mobile implementation begins.

---

## Shared Backend

Web and mobile must use the same backend API.

```text
Angular Web ──────┐
                  │
                  ├── REST API ──→ NestJS ──→ PostgreSQL
                  │
Mobile App ───────┘
```

Neither client should contain independent copies of the core business rules.

For example, the logic for determining today's training belongs to the backend:

```text
GET /api/training/today
```

Both clients consume the same response.

---

## Single Source of Truth

There should be:

- One backend
- One training data model
- One PostgreSQL database
- One training history

A training session recorded from the mobile application must immediately become part of the same history visible from the web application.

Example:

```text
Mobile
   │
   │ Record swimming session
   ▼
NestJS API
   │
   ▼
PostgreSQL
   │
   └── Training Session
             │
             ├── Mobile can view it
             └── Web can view it
```

---

## Why Mobile Matters

Training is performed in real-world environments rather than primarily at a desk.

The mobile application can eventually make the daily workflow much faster:

```text
Open app
   ↓
See today's training
   ↓
Start training
   ↓
Complete training
   ↓
Enter actual result
   ↓
Save
```

The mobile client should therefore prioritize quick interaction rather than complex administration.

---

## Mobile vs Web Responsibilities

The clients may have different UI priorities while sharing the same backend.

### Web

Better suited for:

- Training plan configuration
- Detailed history
- Statistics
- Reports
- Administration
- Reviewing longer periods

### Mobile

Better suited for:

- Today's training
- Quick session entry
- Training while outside
- Quick notes
- Future GPS/location features
- Future offline recording

The distinction is about user experience, not business ownership.

---

## PWA Consideration

A Progressive Web App can also be considered before committing to a separate native mobile application.

Possible architecture:

```text
Angular
   ↓
PWA
   ↓
NestJS API
   ↓
PostgreSQL
```

A PWA may be sufficient if the initial mobile requirements are limited to:

- Viewing today's training
- Recording sessions
- Adding notes
- Viewing basic history

A dedicated mobile application becomes more useful if we later require:

- Advanced GPS tracking
- Background location
- Wearable integration
- Native device capabilities
- More advanced offline behavior

This decision should be made based on actual requirements rather than adding mobile complexity prematurely.

---

# 26. Proposed Client Stack

The current proposal is:

| Client | Technology | Status |
|---|---|---|
| Web | Angular | Proposed |
| Mobile | Flutter or React Native | To be decided |
| Backend | NestJS + TypeScript | Proposed |
| API | REST + JSON | Proposed |
| ORM | TypeORM | Proposed |
| Database | PostgreSQL | Proposed |

The important architectural decision is already established:

> **Web and mobile are clients of the same backend, not separate applications with separate business logic or databases.**

---

# 27. Updated System Architecture

The overall system is now:

```text
                    ┌──────────────────────┐
                    │    Angular Web App   │
                    └──────────┬───────────┘
                               │
                               │
                    ┌──────────▼───────────┐
                    │    Mobile App        │
                    │  Flutter / RN / PWA  │
                    └──────────┬───────────┘
                               │
                         REST / JSON
                               │
                    ┌──────────▼───────────┐
                    │   NestJS Backend      │
                    │                       │
                    │   Dog                 │
                    │   Exercise            │
                    │   Training Plan       │
                    │   Training Session    │
                    │   Statistics          │
                    └──────────┬────────────┘
                               │
                            TypeORM
                               │
                    ┌──────────▼───────────┐
                    │     PostgreSQL       │
                    └──────────────────────┘
```

---

# 28. Updated Architecture Questions

Additional decisions now required:

- [ ] Decide whether mobile is part of V1 or a later phase.
- [ ] Decide between Flutter and React Native.
- [ ] Evaluate whether an Angular PWA is sufficient for V1.
- [ ] Define mobile-specific requirements.
- [ ] Define offline requirements.
- [ ] Define future GPS requirements.
- [ ] Define future wearable/device integration requirements.

**Current recommendation:** Keep the architecture mobile-ready from the beginning, while avoiding implementation of mobile-specific complexity until the actual mobile use cases are finalized.
