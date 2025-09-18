from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Project, Task, ExpenditureLog, ProjectTeamMembership


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "start_date", "end_date", "budget"]  
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assigned_to", "completed"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
TaskFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskForm, 
    fields=('title', 'description', 'due_date', 'assigned_to', 'completed'),
    extra=1,
    can_delete=True
)

class ProjectTeamMembershipForm(forms.ModelForm):
    class Meta:
        model = ProjectTeamMembership
        fields = ["user", "role"]

TeamFormSet = inlineformset_factory(
    Project,
    ProjectTeamMembership,
    fields=('user', 'role'),
    extra=3,
    can_delete=True
)

class ExpenditureLogForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label="Project")

    class Meta:
        model = ExpenditureLog
        fields = ['project', 'description', 'amount']