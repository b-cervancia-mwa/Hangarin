from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Priority, Task


class SeededDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='hangarinuser',
            password='hangarinpass123',
        )

    def test_required_priorities_are_seeded(self):
        expected = {"high", "medium", "low", "critical", "optional"}
        actual = set(Priority.objects.values_list("name", flat=True))
        self.assertTrue(expected.issubset(actual))

    def test_required_categories_are_seeded(self):
        expected = {"Work", "School", "Personal", "Finance", "Projects"}
        actual = set(Category.objects.values_list("name", flat=True))
        self.assertTrue(expected.issubset(actual))

    def test_starter_task_is_seeded(self):
        task = Task.objects.get(title="Review Hangarin starter data")
        self.assertEqual(task.status, "Pending")
        self.assertEqual(task.priority.name, "high")
        self.assertEqual(task.category.name, "Projects")

    def test_dashboard_renders_seeded_task(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Latest Task Updates")
        self.assertContains(response, "Review Hangarin starter data")
        self.assertContains(response, "Search tasks...")

    def test_task_list_renders_seeded_task(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Tasks")
        self.assertContains(response, "Review Hangarin starter data")

    def test_task_list_recreates_starter_task_when_all_tasks_are_deleted(self):
        self.client.force_login(self.user)
        Task.objects.all().delete()

        response = self.client.get(reverse("task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)
        self.assertContains(response, "Review Hangarin starter data")

    def test_login_page_shows_social_login_buttons(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continue with Google")
        self.assertContains(response, "Continue with GitHub")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logout_redirects_back_to_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

        follow_up = self.client.get(reverse("home"))
        self.assertEqual(follow_up.status_code, 302)
        self.assertIn('/login/', follow_up.url)
