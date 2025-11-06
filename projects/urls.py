from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import project_list, project_create, project_delete, project_detail, project_edit



urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('add/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('register/', views.register, name='register'),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"), 
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('home/', views.home, name='home'),
    path('<int:pk>/delete/', views.project_delete_confirm, name='project_delete_confirm'),
    path('add_expenditure/', views.add_expenditure, name='add_expenditure'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
