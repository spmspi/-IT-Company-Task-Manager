from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline")
    list_filter = ("deadline",)

class WorkerAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        (("Position info", {"fields": ("position",)}),)
    )

admin.site.register(Worker, WorkerAdmin)


