from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from catalog import models


@login_required
def index(request):
    num_tasks = models.Task.objects.all().count()
    num_workers = models.Worker.objects.all().count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }
    return render(request, "manager/index.html", context=context)

