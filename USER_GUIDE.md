# Training Tracker — User Guide

## 1. Introduction

Training Tracker is a simple application for recording a dog's daily training routine.

The basic workflow is:

```text
View today's plan
       ↓
Perform training
       ↓
Record actual result
       ↓
Add notes if needed
       ↓
Save
       ↓
Review history
```

# 2. Getting Started

## 2.1 Create the Dog

Create the dog's basic profile.

Example:

```text
Name: Luna
Breed: Greyhound
```

## 3. Configure the Weekly Training Plan

Define what should happen on each day.

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

The plan can be changed when the routine changes.

Changing the future plan must not modify old training records.

# 4. View Today's Training

The dashboard shows the activity planned for today.

Example:

```text
Today

Swimming
Planned: 20 minutes
```

# 5. Record a Training Session

After training, record the actual result.

Example:

```text
Activity: Swimming

Planned:
20 minutes

Actual:
18 minutes

Status:
Completed
```

Save the record.

# 6. Training Status

### Completed

The planned activity was completed.

```text
Planned: 20 minutes
Actual: 20 minutes
Status: Completed
```

### Partially Completed

The activity happened but did not fully match the plan.

```text
Planned: 20 minutes
Actual: 15 minutes
Status: Partially Completed
```

### Skipped

The planned activity was not performed.

```text
Planned: Swimming — 20 minutes
Actual: 0 minutes
Status: Skipped
```

A reason can be added in the notes.

# 7. Recording Notes

Notes are optional.

Examples:

```text
Good session.
```

```text
Dog was energetic today.
```

```text
Stopped early.
```

Keep notes simple and useful.

# 8. Rest Days

Rest is part of the training plan.

Example:

```text
Thursday
Rest
```

A rest day does not require an exercise duration.

# 9. Reviewing Training History

History contains previous sessions.

Example:

```text
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

Historical records represent what actually happened on that date.

# 10. Weekly Overview

Example:

```text
Monday      Running       ✓
Tuesday     Walking       ✓
Wednesday   Swimming      ✓
Thursday    Rest          ✓
Friday      Running       ○
Saturday    Walking       ○
Sunday      Rest          ○
```

# 11. Basic Statistics

Simple statistics may include:

```text
Training Days: 5
Completed: 4
Skipped: 1
Rest Days: 2
```

Activity totals may also be shown:

```text
Running: 2 sessions
Walking: 2 sessions
Swimming: 1 session
```

For duration-based activities:

```text
Swimming
Sessions: 4
Total: 78 minutes
Average: 19.5 minutes
```

These are descriptive records, not medical or veterinary assessments.

# 12. Changing the Training Plan

If the routine changes, update the weekly plan.

Example:

```text
Previous:
Wednesday → Swimming — 20 minutes

New:
Wednesday → Swimming — 30 minutes
```

Future sessions use the new plan.

Previous records remain unchanged.

# 13. Recommended Daily Workflow

### Morning

Check today's training.

```text
Today's Training
↓
Swimming — 20 minutes
```

### During Training

Perform the planned activity.

### After Training

Record:

- Actual duration or relevant measurement
- Status
- Optional notes

### End of Day

Confirm that the record is saved.

# 14. Example Full Day

Suppose Wednesday is a swimming day.

Before training:

```text
Today's Plan

Swimming
20 minutes
```

After training, the actual session was 18 minutes:

```text
Activity: Swimming
Planned: 20 minutes
Actual: 18 minutes
Status: Partially Completed
Notes: Good session.
```

# 15. Example Week

```text
Monday
Running
Completed

Tuesday
Walking
Completed

Wednesday
Swimming
18 / 20 minutes
Partially Completed

Thursday
Rest
Completed

Friday
Running
Completed

Saturday
Walking
Skipped

Sunday
Rest
Completed
```

# 16. Important Usage Principles

### Record what actually happened

Do not change the actual result just to match the plan.

### Keep notes short

Use notes for useful observations.

### Preserve history

Changing the future schedule must not change previous records.

### Keep the routine practical

The application should support the training process rather than make it more complicated.

# 17. Future Features

Possible future capabilities:

- Distance tracking
- Running speed and pace
- Hill repetitions
- More detailed activity measurements
- Training charts
- Monthly reports
- Race information
- Training phases
- GPS tracking
- Wearable data
- Notifications
- Multiple dogs

These are not required for V1.

# 18. Current V1 Workflow

```text
Create Dog
    ↓
Create Weekly Training Plan
    ↓
Open Dashboard
    ↓
View Today's Training
    ↓
Perform Training
    ↓
Record Actual Result
    ↓
Set Status
    ↓
Add Optional Notes
    ↓
Save
    ↓
Review History
```

This is the primary workflow of Training Tracker.
