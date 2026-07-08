from multiprocessing import context

from django.contrib.auth.models import AbstractUser
from django.views import generic, View
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Task, Worker
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from catalog import models
from catalog.forms import TaskCreateForm, WorkerCreateForm, SearchTaskForm, SearchWorkerForm


@login_required
def index(request):
    num_tasks = models.Task.objects.all().count()
    num_workers = models.Worker.objects.all().count()
    active_tasks = models.Task.objects.filter(is_completed=False).count()
    complete_tasks = models.Task.objects.filter(is_completed=True).count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "active_tasks": active_tasks,
        "complete_tasks": complete_tasks,
    }
    return render(request, "catalog/index.html", context=context)

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_forms"] = SearchTaskForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Task.objects.filter(name__icontains=name)
        return Task.objects.all()


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "catalog/task_form.html"
    success_url = reverse_lazy("catalog:task-list")

class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("catalog:task-list")
    template_name = "catalog/task_confirm_delete.html"

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "catalog/task_detail.html"

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = "catalog/task_form.html"
    form_class = TaskCreateForm
    success_url = reverse_lazy("catalog:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "catalog/worker_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_forms"] = SearchWorkerForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        username = self.request.GET.get("username")
        if username:
            return Worker.objects.filter(username__icontains=username)
        return Worker.objects.all()


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    template_name = "catalog/worker_form.html"
    success_url = reverse_lazy("catalog:worker-list")

class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "catalog/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        context["complete_task"] = worker.assigned_tasks.filter(is_completed=True)
        context["active_task"] = worker.assigned_tasks.filter(is_completed=False)
        return context

class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("catalog:worker-list")
    template_name = "catalog/worker_confirm_delete.html"

class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "email", "position"]
    template_name = "catalog/worker_form.html"
    success_url = reverse_lazy("catalog:worker-list")

class TaskWorkerToggle(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        current_worker = request.user
        if current_worker in task.assignees.all():
            task.assignees.remove(current_worker)
        else:
            task.assignees.add(current_worker)
        return redirect("catalog:task-detail", pk=pk)

class MyTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    context_object_name = "my_task_list"
    template_name = "catalog/my_task_list.html"
    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)

class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return redirect("catalog:my-task-list")