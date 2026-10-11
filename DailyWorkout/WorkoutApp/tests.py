from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import (
    Dog,
    ExerciseType,
    SessionStatus,
    TrainingSession,
    Weekday,
    WeeklyWorkoutPlan,
    WeeklyWorkoutPlanDay,
)


class WorkoutStructureTests(TestCase):
    def setUp(self):
        self.running, _ = ExerciseType.objects.get_or_create(
            name="Running",
            defaults={"is_rest": False},
        )
        self.rest, _ = ExerciseType.objects.get_or_create(
            name="Rest",
            defaults={"is_rest": True},
        )
        self.luna = Dog.objects.create(name="Luna", breed="Greyhound")
        self.milo = Dog.objects.create(name="Milo", breed="Greyhound")

    def test_admin_can_keep_many_dogs_and_named_plans(self):
        plan_a = WeeklyWorkoutPlan.objects.create(
            dog=self.luna,
            name="Workout Plan A",
            is_active=True,
        )
        WeeklyWorkoutPlanDay.objects.create(
            plan=plan_a,
            weekday=Weekday.MONDAY,
            exercise_type=self.running,
        )
        WeeklyWorkoutPlanDay.objects.create(
            plan=plan_a,
            weekday=Weekday.THURSDAY,
            exercise_type=self.rest,
        )

        self.assertEqual(Dog.objects.count(), 2)
        self.assertEqual(self.luna.active_plan().name, "Workout Plan A")
        self.assertEqual(plan_a.days.count(), 2)
        self.assertTrue(plan_a.days.get(weekday=Weekday.THURSDAY).exercise_type.is_rest)

    def test_activating_a_plan_deactivates_the_previous_one_for_that_dog(self):
        first = WeeklyWorkoutPlan.objects.create(
            dog=self.luna,
            name="Workout Plan A",
            is_active=True,
        )
        second = WeeklyWorkoutPlan.objects.create(
            dog=self.luna,
            name="Workout Plan B",
            is_active=True,
        )
        milo_plan = WeeklyWorkoutPlan.objects.create(
            dog=self.milo,
            name="Workout Plan A",
            is_active=True,
        )

        first.refresh_from_db()
        self.assertFalse(first.is_active)
        self.assertTrue(second.is_active)
        self.assertTrue(milo_plan.is_active)
        self.assertEqual(self.luna.active_plan(), second)

    def test_a_plan_day_allows_only_one_exercise(self):
        plan = WeeklyWorkoutPlan.objects.create(dog=self.luna, name="Workout Plan A")
        WeeklyWorkoutPlanDay.objects.create(
            plan=plan,
            weekday=Weekday.MONDAY,
            exercise_type=self.running,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                WeeklyWorkoutPlanDay.objects.create(
                    plan=plan,
                    weekday=Weekday.MONDAY,
                    exercise_type=self.rest,
                )

    def test_editing_the_plan_does_not_change_a_saved_session(self):
        plan = WeeklyWorkoutPlan.objects.create(
            dog=self.luna,
            name="Workout Plan A",
            is_active=True,
        )
        monday = WeeklyWorkoutPlanDay.objects.create(
            plan=plan,
            weekday=Weekday.MONDAY,
            exercise_type=self.running,
        )
        session = TrainingSession.objects.create(
            dog=self.luna,
            date=date(2026, 10, 5),
            plan=plan,
            exercise_type=self.running,
            status=SessionStatus.COMPLETED,
            notes="Good session.",
        )

        monday.exercise_type = self.rest
        monday.save()
        self.rest.name = "Recovery"
        self.rest.save()
        session.refresh_from_db()

        self.assertEqual(session.exercise_name, "Running")
        self.assertFalse(session.is_rest)
        self.assertEqual(session.status, SessionStatus.COMPLETED)
        self.assertEqual(monday.exercise_type, self.rest)

    def test_rest_session_is_stored_as_a_whole_day_rest(self):
        session = TrainingSession.objects.create(
            dog=self.luna,
            date=date(2026, 10, 8),
            exercise_type=self.rest,
            status=SessionStatus.COMPLETED,
        )
        session.refresh_from_db()
        self.assertEqual(session.exercise_name, "Rest")
        self.assertTrue(session.is_rest)


class SeededExerciseTypeTests(TestCase):
    def test_initial_exercise_types_include_whole_day_rest(self):
        names = set(ExerciseType.objects.values_list("name", flat=True))
        self.assertTrue(
            {"Running", "Walking", "Swimming", "Hill Climbing", "Rest"} <= names
        )
        self.assertTrue(ExerciseType.objects.get(name="Rest").is_rest)
        self.assertFalse(ExerciseType.objects.get(name="Swimming").is_rest)


class AdminStructureTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username="trainer",
            password="test-only-password",
            email="trainer@example.com",
        )
        self.client.force_login(self.admin_user)

    def test_admin_lists_dogs_plans_exercises_and_sessions(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dogs")
        self.assertContains(response, "Weekly workout plans")
        self.assertContains(response, "Exercise types")
        self.assertContains(response, "Training sessions")

    def test_admin_can_add_a_dog(self):
        response = self.client.post(
            "/admin/WorkoutApp/dog/add/",
            {
                "name": "Luna",
                "breed": "Greyhound",
                "date_of_birth": "",
                "notes": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dog.objects.filter(name="Luna", breed="Greyhound").exists())
