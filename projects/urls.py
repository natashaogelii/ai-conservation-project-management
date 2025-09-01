from django.urls import path
from . import views
from .views import ProjectUpdateView

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('add/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project-detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('register/', views.register, name='register'),
    path("login/", views.login_view, name="login"),

]
