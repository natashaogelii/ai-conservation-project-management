from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ExpenditureLog, Task
from .forms import ProjectForm 
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import TaskForm, ExpenditureLogForm, TeamFormSet, TaskFormSet
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from django.shortcuts import render

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        team_formset = TeamFormSet(request.POST)
        task_formset = TaskFormSet(request.POST)

        if form.is_valid() and team_formset.is_valid() and task_formset.is_valid():
            project = form.save()

            #save teams
            team_formset.instance = project
            team_formset.save()

            # save tasks
            task_formset.instance = project
            task_formset.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
        team_formset = TeamFormSet()
        task_formset = TaskFormSet()
    

    return render(request, 'projects/project_form.html', {
        'form': form,
        'team_formset': team_formset,
        'task_formset': task_formset
    })


# Create your views here.
    
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')  # safe
    return redirect('home')


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
            return redirect("home")  # redirect to the home/dashboard page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "projects/login.html")


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    expenses = project.expenses.all()

    # Forms
    task_form = TaskForm(request.POST or None)
    expense_form = ExpenditureLogForm(request.POST or None)

    if request.method == "POST":
        if "add_task" in request.POST and task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.project = project
            new_task.save()
            return redirect("project_detail", pk=pk)

        if "add_expense" in request.POST and expense_form.is_valid():
            new_expense = expense_form.save(commit=False)
            new_expense.project = project
            new_expense.save()
            return redirect("project_detail", pk=pk)

    context = {
        "project": project,
        "tasks": tasks,
        "expenses": expenses,
        "task_form": task_form,
        "expense_form": expense_form,
    }
    return render(request, "projects/project_detail.html", context)

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        team_formset = TeamFormSet(request.POST, instance=project)
        task_formset = TaskFormSet(request.POST, instance=project)

        if form.is_valid() and team_formset.is_valid() and task_formset.is_valid():
            form.save()
            team_formset.save()
            task_formset.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
        team_formset = TeamFormSet(instance=project)
        task_formset = TaskFormSet(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': form,
        'team_formset': team_formset,
        'task_formset': task_formset,
    })

# views.py
def add_expenditure(request):
    if request.method == "POST":
        form = ExpenditureLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # or 'project_list'
    else:
        form = ExpenditureLogForm()

    return render(request, 'projects/add_expenditure.html', {'form': form})


def home(request):
    user = request.user
    projects = user.projects.all()  # projects user is part of

    # Optional: search
    query = request.GET.get('q')
    if query:
        projects = projects.filter(title__icontains=query)

    # Pending tasks **for the logged-in user only**
    pending_tasks = []
    for project in projects:
        for task in project.tasks.filter(completed=False, assigned_to=user):
            pending_tasks.append({
                'project': project,
                'task': task
            })

    context = {
        'user': user,
        'projects': projects,
        'pending_tasks': sorted(pending_tasks, key=lambda x: x['task'].due_date)
    }
    return render(request, 'projects/home.html', context)

def project_delete_confirm(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')  # or 'project_list', whichever you prefer
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

def dashboard(request):
    projects = Project.objects.all()
    total_projects = projects.count()
    total_budget = sum(p.budget for p in projects)
    total_spent = sum(p.total_spent for p in projects)
    remaining_budget = total_budget - total_spent
    avg_progress = sum(p.progress for p in projects) / total_projects if total_projects else 0

    context = {
        "total_projects": total_projects,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "avg_progress": round(avg_progress, 2),
        "projects": projects,
    }
    return render(request, "projects/dashboard.html", context)

