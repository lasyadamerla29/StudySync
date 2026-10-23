from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Habit, Task

class StudySyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student1", password="StrongPass123!")
        self.client.login(username="student1", password="StrongPass123!")

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_dashboard_loads_for_logged_in_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_user_only_sees_own_tasks(self):
        other = User.objects.create_user(username="student2", password="StrongPass123!")
        Task.objects.create(user=other, title="Private task")
        response = self.client.get(reverse("tasks"))
        self.assertNotContains(response, "Private task")

    def test_create_habit_model(self):
        habit = Habit.objects.create(user=self.user, name="Read 20 minutes")
        self.assertEqual(habit.name, "Read 20 minutes")
