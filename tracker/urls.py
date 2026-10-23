from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("habits/", views.habit_list, name="habits"),
    path("habits/add/", views.habit_add, name="habit_add"),
    path("habits/<int:habit_id>/toggle/", views.habit_toggle, name="habit_toggle"),
    path("habits/<int:habit_id>/delete/", views.habit_delete, name="habit_delete"),
    path("tasks/", views.task_list, name="tasks"),
    path("tasks/add/", views.task_add, name="task_add"),
    path("tasks/<int:task_id>/toggle/", views.task_toggle, name="task_toggle"),
    path("tasks/<int:task_id>/delete/", views.task_delete, name="task_delete"),
    path("study/", views.study_list, name="study"),
    path("reports/", views.reports, name="reports"),
]
