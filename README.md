# Training Tracker

A simple application for tracking a Greyhound's daily training routine.

The first version focuses on a practical workflow:

**Plan training → Perform training → Record actual result → Review history**

## Project Goal

Training Tracker should make it easy to answer:

- What training is planned today?
- What was actually completed?
- How much was completed?
- Was the session completed, partially completed, or skipped?
- What notes were recorded?
- What did the training history look like over time?

## Initial Training Routine

Example weekly routine:

| Day | Training |
|---|---|
| Monday | Running |
| Tuesday | Walking |
| Wednesday | Swimming — 20 minutes |
| Thursday | Rest |
| Friday | Running |
| Saturday | Walking |
| Sunday | Rest |

The schedule is configurable and should not be hard-coded.

## Core Concepts

### Dog

Basic information about the dog.

Example:

```text
Name: Luna
Breed: Greyhound
```

### Exercise Type

Initial types:

- Running
- Walking
- Swimming
- Hill Climbing
- Rest

### Training Plan

Defines what should happen on each day.

Example:

```text
Wednesday → Swimming → 20 minutes
```

### Training Session

Records what actually happened.

Example:

```text
Date: 29 Sep 2026
Activity: Swimming
Planned: 20 minutes
Actual: 18 minutes
Status: Completed
Notes: Good session
```

## Planned vs Actual

The application intentionally separates planned training from actual training.

```text
Planned:
Swimming — 20 minutes

Actual:
Swimming — 18 minutes

Status:
Completed
```

This preserves both the original plan and the real result.

## V1 Scope

- Create a dog
- Configure a weekly training plan
- View today's training
- Record a training session
- Record actual duration where applicable
- Mark sessions completed, partially completed, or skipped
- Add notes
- View training history
- View the current week's status
- View basic statistics

## Out of Scope for V1

- GPS tracking
- Wearable integration
- Heart-rate monitoring
- Medical diagnosis
- Automatic injury detection
- AI-generated training plans
- Race prediction
- Advanced performance analytics
- Complex nutrition management
- Social features

## Development Approach

```text
Requirements
    ↓
Use Cases
    ↓
Domain Model
    ↓
Database Design
    ↓
Backend
    ↓
Frontend
    ↓
Integration
    ↓
Testing
    ↓
V1 Release
```

Development will be incremental and issue-driven.

## Documentation

- [`PLAN.md`](./PLAN.md) — project scope, roadmap, milestones, decisions, and development tracking.
- [`USER_GUIDE.md`](./USER_GUIDE.md) — how to use the application.

## Current Status

**Version:** V1 — Initial Planning

**Status:** Requirements / Use-case discussion

**Next milestone:** Finalize V1 use cases and domain model.

## Project Principles

1. Keep daily usage simple.
2. Record planned and actual training separately.
3. Preserve historical records.
4. Avoid unnecessary data collection.
5. Build the smallest useful version first.
6. Add complexity only when the real training workflow requires it.
