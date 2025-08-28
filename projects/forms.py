from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'department', 'description', 'start_date', 'end_date', 'progress']
