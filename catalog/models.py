from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    class TaskTypeChoices(models.TextChoices):
        bug = "Bug", "Bug"
        new_feature = "New_feature", "New feature"
        breaking_change = "Breaking_change", "Breaking change"
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
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="workers")

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
