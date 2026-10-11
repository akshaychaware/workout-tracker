from django.contrib import admin

from .models import Dog, ExerciseType, TrainingSession, WeeklyWorkoutPlan, WeeklyWorkoutPlanDay

admin.site.site_header = "Training Tracker"
admin.site.site_title = "Training Tracker"
admin.site.index_title = "Dogs and workout plans"


class WeeklyWorkoutPlanDayInline(admin.TabularInline):
    model = WeeklyWorkoutPlanDay
    extra = 7
    max_num = 7
    fields = ("weekday", "exercise_type")


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "date_of_birth", "active_plan")
    search_fields = ("name", "breed")
    ordering = ("name",)

    @admin.display(description="Active plan")
    def active_plan(self, obj):
        plan = obj.active_plan()
        if plan is None:
            return "—"
        return plan.name


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_rest")
    list_filter = ("is_rest",)
    search_fields = ("name",)


@admin.register(WeeklyWorkoutPlan)
class WeeklyWorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "dog", "is_active", "updated_at")
    list_filter = ("is_active", "dog")
    search_fields = ("name", "dog__name")
    autocomplete_fields = ("dog",)
    inlines = (WeeklyWorkoutPlanDayInline,)


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ("date", "dog", "exercise_name", "is_rest", "status")
    list_filter = ("status", "is_rest", "dog")
    search_fields = ("dog__name", "exercise_name", "notes")
    autocomplete_fields = ("dog", "plan", "exercise_type")
    readonly_fields = ("exercise_name", "is_rest")
    date_hierarchy = "date"
