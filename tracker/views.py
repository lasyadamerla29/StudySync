from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Sum
from .forms import RegisterForm, HabitForm, TaskForm, StudySessionForm
from .models import Habit, HabitCompletion, Task, StudySession

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to StudySync! Your account is ready.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    habits = Habit.objects.filter(user=request.user, is_active=True)
    completed_habit_ids = set(HabitCompletion.objects.filter(
        habit__user=request.user, date=today
    ).values_list("habit_id", flat=True))
    tasks = Task.objects.filter(user=request.user)
    sessions = StudySession.objects.filter(user=request.user, studied_on__gte=week_start, studied_on__lte=today)
    week_minutes = sessions.aggregate(total=Sum("minutes"))["total"] or 0
    context = {
        "today": today,
        "habits": habits,
        "completed_habit_ids": completed_habit_ids,
        "tasks": tasks[:6],
        "pending_count": tasks.filter(completed=False).count(),
        "completed_count": tasks.filter(completed=True).count(),
        "week_hours": round(week_minutes / 60, 1),
        "week_sessions": sessions.count(),
        "habit_done": len(completed_habit_ids),
        "habit_total": habits.count(),
    }
    return render(request, "tracker/dashboard.html", context)

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user, is_active=True)
    today = timezone.localdate()
    completed_ids = set(HabitCompletion.objects.filter(habit__user=request.user, date=today).values_list("habit_id", flat=True))
    return render(request, "tracker/habits.html", {"habits": habits, "completed_ids": completed_ids})

@login_required
def habit_add(request):
    form = HabitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        habit = form.save(commit=False)
        habit.user = request.user
        habit.save()
        messages.success(request, "Habit created.")
        return redirect("habits")
    return render(request, "tracker/form.html", {"form": form, "heading": "Add a habit", "cancel_url": "habits"})

@login_required
def habit_toggle(request, habit_id):
    if request.method != "POST":
        return redirect("habits")
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    today = timezone.localdate()
    completion, created = HabitCompletion.objects.get_or_create(habit=habit, date=today)
    if not created:
        completion.delete()
        messages.info(request, "Habit marked as not completed.")
    else:
        messages.success(request, "Nice work — habit completed for today!")
    return redirect(request.POST.get("next") if request.POST.get("next") in ["dashboard", "habits"] else "habits")

@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    if request.method == "POST":
        habit.delete()
        messages.success(request, "Habit deleted.")
    return redirect("habits")

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tracker/tasks.html", {"tasks": tasks})

@login_required
def task_add(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Task added.")
        return redirect("tasks")
    return render(request, "tracker/form.html", {"form": form, "heading": "Add a task", "cancel_url": "tasks"})

@login_required
def task_toggle(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.completed = not task.completed
        task.save(update_fields=["completed"])
        messages.success(request, "Task status updated.")
    return redirect("tasks")

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
    return redirect("tasks")

@login_required
def study_list(request):
    sessions = StudySession.objects.filter(user=request.user)
    form = StudySessionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        session = form.save(commit=False)
        session.user = request.user
        session.save()
        messages.success(request, "Study session recorded.")
        return redirect("study")
    total_minutes = sessions.aggregate(total=Sum("minutes"))["total"] or 0
    return render(request, "tracker/study.html", {"sessions": sessions[:30], "form": form, "total_hours": round(total_minutes / 60, 1)})

@login_required
def reports(request):
    today = timezone.localdate()
    start = today - timedelta(days=6)
    sessions = StudySession.objects.filter(user=request.user, studied_on__gte=start, studied_on__lte=today)
    daily = []
    for offset in range(7):
        day = start + timedelta(days=offset)
        minutes = sessions.filter(studied_on=day).aggregate(total=Sum("minutes"))["total"] or 0
        daily.append({"date": day, "minutes": minutes, "hours": round(minutes / 60, 1), "percent": min(100, round(minutes / 6))})
    tasks = Task.objects.filter(user=request.user)
    total_habits = Habit.objects.filter(user=request.user, is_active=True).count()
    completions = HabitCompletion.objects.filter(habit__user=request.user, date__gte=start, date__lte=today).count()
    return render(request, "tracker/reports.html", {
        "daily": daily,
        "week_hours": round(sum(x["minutes"] for x in daily) / 60, 1),
        "completed_tasks": tasks.filter(completed=True).count(),
        "pending_tasks": tasks.filter(completed=False).count(),
        "active_habits": total_habits,
        "habit_completions": completions,
    })
