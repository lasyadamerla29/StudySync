from django.conf import settings
from django.db import models
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="completions")
    date = models.DateField(default=timezone.localdate)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["habit", "date"], name="unique_habit_completion_per_day")
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.habit.name} — {self.date}"

class Task(models.Model):
    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["completed", "due_date", "-created_at"]

    def __str__(self):
        return self.title

class StudySession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_sessions")
    subject = models.CharField(max_length=100)
    minutes = models.PositiveIntegerField()
    studied_on = models.DateField(default=timezone.localdate)
    notes = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-studied_on", "-created_at"]

    def __str__(self):
        return f"{self.subject} ({self.minutes} min)"
