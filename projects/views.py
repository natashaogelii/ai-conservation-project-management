from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm 
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

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