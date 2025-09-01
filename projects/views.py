from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm 
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

# Create your views here.
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'description', 'status']  # include any other fields you want editable
    template_name = 'projects/project_update.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})
    
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":  # confirmation form submitted
        project.delete()
        return redirect('project_list')  # back to all projects

    return render(request, 'projects/project_confirm_delete.html', {'project': project})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "projects/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("project_list")  # goes to home/projects page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "projects/login.html")


