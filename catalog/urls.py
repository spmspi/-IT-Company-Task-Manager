from multiprocessing.pool import worker

from django.urls import path

from catalog.views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    WorkerListView,
    WorkerCreateView,
    WorkerDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/",
         TaskListView.as_view(),
         name="task-list"),
    path(
    "task/create/",
    TaskCreateView.as_view(),
    name="task-create"
    ),
    path("task/<int:pk>/",
         TaskDetailView.as_view(),
         name="task-detail"),
    path("worker/",
         WorkerListView.as_view(),
         name="worker-list"),
    path(
    "worker/create/",
    WorkerCreateView.as_view(),
    name="worker-create"
    ),
    path("worker/<int:pk>/",
         WorkerDetailView.as_view(),
         name="worker-detail"),

]

app_name = "catalog"