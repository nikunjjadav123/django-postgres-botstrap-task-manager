
from .models import Task
from .forms import TaskForm
from django.shortcuts import render, redirect, get_object_or_404

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            tasks = Task.objects.all()
            return render(request, "tasks/task_list.html", {"tasks": tasks})
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form})

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)   # fetch task by primary key
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
