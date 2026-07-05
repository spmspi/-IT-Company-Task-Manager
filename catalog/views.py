from django.views import generic
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Task
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from catalog import models
from catalog.forms import TaskCreateForm


@login_required
def index(request):
    num_tasks = models.Task.objects.all().count()
    num_workers = models.Worker.objects.all().count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }
    return render(request, "manager/index.html", context=context)

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "manager/task_list.html"
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Task.objects.filter(name__icontains=name)
        return Task.objects.all()


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("catalog:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    pass

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    pass

class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    pass

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass

class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass
