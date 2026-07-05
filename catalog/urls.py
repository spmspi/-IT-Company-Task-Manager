from django.urls import path

from catalog.views import index, TaskListView, TaskCreateView

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
]

app_name = "catalog"