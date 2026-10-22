from django.test import TestCase
from rest_framework.test import APIClient

from tasks.models import Task


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_and_list_open_tasks(self):
        response = self.client.post(
            "/api/tasks/",
            {"title": "Vueを学ぶ", "description": "SPA"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)

        Task.objects.create(title="完了済み", is_done=True)

        response = self.client.get("/api/tasks/?status=open")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "Vueを学ぶ")

    def test_toggle_and_delete(self):
        task = Task.objects.create(title="切替テスト")
        response = self.client.post(f"/api/tasks/{task.pk}/toggle/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_done"])

        response = self.client.delete(f"/api/tasks/{task.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)

    def test_invalid_status_filter(self):
        response = self.client.get("/api/tasks/?status=unknown")
        self.assertEqual(response.status_code, 400)
