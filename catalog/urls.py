from multiprocessing.pool import worker

from django.urls import path

from catalog.views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskDeleteView,
    TaskUpdateView,
    WorkerListView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerDeleteView,
    WorkerUpdateView,
    TaskWorkerToggle,
    MyTaskListView,
    TaskToggleCompleteView,
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
    path("task/<int:pk>/delete/",
         TaskDeleteView.as_view(),
         name="task-delete"),
    path("task/<int:pk>/update/",
         TaskUpdateView.as_view(),
         name="task-update"),
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
    path("worker/<int:pk>/delete/",
         WorkerDeleteView.as_view(),
         name="worker-delete"),
    path("worker/<int:pk>/update/",
         WorkerUpdateView.as_view(),
         name="worker-update"),
    path("task/<int:pk>/TaskWorkerToggle/",
         TaskWorkerToggle.as_view(),
         name="task-worker-toggle"),
    path("my-task/",
         MyTaskListView.as_view(),
         name="my-task-list"),
    path("tasks/<int:pk>/toggle-complete/",
         TaskToggleCompleteView.as_view(),
         name="task-toggle-complete"),

]

app_name = "catalog"