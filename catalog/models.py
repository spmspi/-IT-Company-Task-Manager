from datetime import timedelta, datetime
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    class TaskTypeChoices(models.TextChoices):
        bug = "Bug", "Bug"
        new_feature = "New feature", "New feature"
        breaking_change = "Breaking change", "Breaking change"
        refactoring = "Refactoring", "Refactoring"
        QA = "QA", "QA"

    name = models.CharField(
        max_length=25,
        choices=TaskTypeChoices.choices,
        default=TaskTypeChoices.new_feature,
    )
    def __str__(self):
        return self.name



class Position(models.Model):
    name = models.CharField(max_length=255,)


class Worker(AbstractUser):
    class PositionChoices(models.TextChoices):
        DEVELOPER = "DEVELOPER", "Developer"
        Project_Manager = "Project_Manager", "Project Manager"
        QA = "QA", "QA"
        Designer = "Designer", "Designer"
        DevOPS = "DevOPS", "DevOPS"
    position = models.CharField(
        max_length=25,
        choices=PositionChoices.choices,
        blank=True,
        null=True,
        default=PositionChoices.DEVELOPER,
    )

    def __str__(self):
        return self.username


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="assigned_tasks")

    def __str__(self):
        return self.name

    @property
    def is_urgent(self):
        now = timezone.now()
        time_limit = now + timedelta(hours=1)
        if self.deadline > now and self.deadline <= time_limit:
            return True
        return False

