from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import Worker, Task, TaskType, Position


class ModelTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="QA")
        self.assertEqual(
            str(position), f"{position.name}")

    def test_worker_str(self):
        self.position = Position.objects.create(name="QA")
        worker = get_user_model().objects.create_user(
            first_name="test",
            last_name="test",
            username="test",
            email="test@test.tes",
            password="Test123",
            position=self.position,
        )

        self.assertEqual(
            str(worker),
            f"{worker.username}"

        )

    def test_car_str(self):
        position = Position.objects.create(name="QA")
        worker1 = get_user_model().objects.create_user(
            first_name="test",
            last_name="test",
            username="test",
            email="test@test.tes",
            password="Test123",
            position=position,
        )
        self.task_type = TaskType.objects.create(name="QA")
        self.task1 = Task.objects.create(
            name="test",
            description="Test description",
            deadline="2026-07-12 12:20",
            is_completed="False",
            priority="Medium",
            task_type=self.task_type,
        )
        self.task1.assignees.add(worker1)
        self.assertEqual(str(self.task1), "test")