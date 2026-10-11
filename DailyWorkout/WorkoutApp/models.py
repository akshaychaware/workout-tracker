from django.db import models, transaction


class Weekday(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"


class SessionStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    COMPLETED = "completed", "Completed"
    PARTIALLY_COMPLETED = "partially_completed", "Partially Completed"
    SKIPPED = "skipped", "Skipped"


class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name

    def active_plan(self):
        return self.workout_plans.filter(is_active=True).first()


class ExerciseType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_rest = models.BooleanField(
        default=False,
        help_text="Whole-day rest. The dog does no exercise on a day that uses this type.",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if self.is_rest:
            return f"{self.name} (whole-day rest)"
        return self.name


class WeeklyWorkoutPlan(models.Model):
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="workout_plans",
    )
    name = models.CharField(
        max_length=100,
        help_text="For example, Workout Plan A. Edit this plan, or add another one.",
    )
    is_active = models.BooleanField(
        default=False,
        help_text="The plan currently used for this dog. Only one plan per dog can be active.",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["dog__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["dog", "name"],
                name="unique_plan_name_per_dog",
            ),
        ]

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"{self.dog}: {self.name} ({status})"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_active and self.dog_id:
                WeeklyWorkoutPlan.objects.filter(
                    dog_id=self.dog_id,
                    is_active=True,
                ).exclude(pk=self.pk).update(is_active=False)
            super().save(*args, **kwargs)


class WeeklyWorkoutPlanDay(models.Model):
    plan = models.ForeignKey(
        WeeklyWorkoutPlan,
        on_delete=models.CASCADE,
        related_name="days",
    )
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    exercise_type = models.ForeignKey(
        ExerciseType,
        on_delete=models.PROTECT,
        related_name="plan_days",
    )

    class Meta:
        ordering = ["weekday"]
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "weekday"],
                name="one_exercise_per_plan_day",
            ),
        ]

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.exercise_type.name}"


class TrainingSession(models.Model):
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="training_sessions",
    )
    date = models.DateField()
    plan = models.ForeignKey(
        WeeklyWorkoutPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="training_sessions",
        help_text="Plan in effect when this session was recorded. Later plan edits do not change this session.",
    )
    exercise_type = models.ForeignKey(
        ExerciseType,
        on_delete=models.PROTECT,
        related_name="training_sessions",
    )
    exercise_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Copied from the exercise when this session is saved.",
    )
    is_rest = models.BooleanField(
        default=False,
        help_text="Copied from the exercise. True means this date was a whole-day rest.",
    )
    status = models.CharField(
        max_length=32,
        choices=SessionStatus.choices,
        default=SessionStatus.PLANNED,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "dog__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["dog", "date"],
                name="one_session_per_dog_per_day",
            ),
        ]

    def __str__(self):
        return f"{self.date}: {self.dog} — {self.exercise_name or self.exercise_type.name}"

    def save(self, *args, **kwargs):
        if self.exercise_type_id:
            exercise = self.exercise_type
            self.exercise_name = exercise.name
            self.is_rest = exercise.is_rest
        super().save(*args, **kwargs)
