from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Habit, Task, StudySession

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class HabitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Habit
        fields = ("name", "description")
        widgets = {"description": forms.TextInput(attrs={"placeholder": "Optional note"})}

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Task
        fields = ("title", "description", "due_date", "priority")
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class StudySessionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = StudySession
        fields = ("subject", "minutes", "studied_on", "notes")
        widgets = {
            "studied_on": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.TextInput(attrs={"placeholder": "Optional notes"}),
        }
