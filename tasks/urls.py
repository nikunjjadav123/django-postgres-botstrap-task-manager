from django.urls import path
from django.shortcuts import redirect
from tasks import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('', views.home, name='home'),
    path('task/add/', views.add_task, name='task_create'),
    path('task/<int:pk>/edit/', views.edit_task, name='task_update'),
    path('task/<int:pk>/delete/', views.delete_task, name='task_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]
