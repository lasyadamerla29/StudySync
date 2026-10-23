from django.contrib import admin
from .models import Habit, HabitCompletion, Task, StudySession

admin.site.register(Habit)
admin.site.register(HabitCompletion)
admin.site.register(Task)
admin.site.register(StudySession)
