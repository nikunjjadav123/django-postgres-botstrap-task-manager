from django.urls import path
from django.shortcuts import redirect
from tasks import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('', views.home, name='home'),
    path('task/add/', views.add_task, name='task_create'),
    path('task/<int:pk>/edit/', views.edit_task, name='task_update'),
    path('task/<int:pk>/delete/', views.delete_task, name='task_delete'),
    path('login/', views.jwt_login_page, name='login'),
    path('logout/', views.jwt_logout_page, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/edit/', views.update_profile, name='profile_update'),
    path("api/tasks/", views.user_tasks_json, name="tasks_json"),
]
