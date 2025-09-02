from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/add/', views.add_task, name='task_create'),
    path('task/<int:pk>/edit/', views.edit_task, name='task_update'),
    path('task/<int:pk>/delete/', views.delete_task, name='task_delete'),
]
