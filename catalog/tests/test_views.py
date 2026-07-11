from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Worker, Task, TaskType, Position

URL_TASK_URL = reverse("catalog:task-list")
URL_WORKER_URL = reverse("catalog:worker-list")


class PublicWorkerTest(TestCase):

    def test_login_required(self):
        res = self.client.get(URL_WORKER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="QA")
        self.user = get_user_model().objects.create_user(
            first_name="test",
            last_name="test",
            username="test",
            email="test@test.tes",
            password="Test123",
            position=self.position,
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="QA")
        self.task_type2 = TaskType.objects.create(name="Bug")
        self.task1 = Task.objects.create(
            name="test",
            description="Test description",
            deadline="2026-07-12 12:20",
            is_completed="False",
            priority="Medium",
            task_type=self.task_type,
            )
        self.task2 = Task.objects.create(
            name="1234",
            description="Test description",
            deadline="2026-07-12 12:20",
            is_completed="False",
            priority="Priority",
            task_type=self.task_type2,
        )

    def test_worker_list(self):
        response = self.client.get(URL_WORKER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/worker_list.html")

    def test_search_manufacturer_load(self):
        res = URL_TASK_URL
        response = self.client.get(res, {"name": "tes"})
        self.assertEqual(response.status_code, 200)

    def test_search_task(self):
        task1 = Task.objects.create(
            name="Onetask",
            description="Test description",
            deadline="2026-07-12 12:20",
            is_completed="False",
            priority="Priority",
            task_type=self.task_type2,
        )
        task2 = Task.objects.create(
            name="1234",
            description="Test description",
            deadline="2026-07-12 12:20",
            is_completed="False",
            priority="Priority",
            task_type=self.task_type,
        )
        response = self.client.get(URL_TASK_URL, {"name": "one"})
        self.assertIn(task1, response.context["task_list"])
        self.assertNotIn(task2, response.context["task_list"])

    def test_search_driver(self):
        worker1 = get_user_model().objects.create_user(
            first_name="testsearch",
            last_name="test",
            username="testsearch",
            email="test123@test.tes",
            password="Test123",
            position=self.position,
        )
        worker2 = get_user_model().objects.create_user(
            first_name="123",
            last_name="321",
            username="TwoUserSearch",
            email="123@123.tes",
            password="Test123@723%%",
            position=self.position,
        )
        response = self.client.get(URL_WORKER_URL, {"username": "two"})
        self.assertIn(worker2, response.context["worker_list"])
        self.assertNotIn(worker1, response.context["worker_list"])

