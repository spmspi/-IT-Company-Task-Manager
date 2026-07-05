from django import forms
from django.contrib.auth import get_user_model

from catalog.models import Task


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = ["name",
                  "task_type",
                  "description",
                  "priority",
                  "deadline",
                  "assignees",
                  ]
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local",
                       "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.deadline:
            self.fields['deadline'].initial = self.instance.deadline.strftime("%Y-%m-%dT%H:%M")
