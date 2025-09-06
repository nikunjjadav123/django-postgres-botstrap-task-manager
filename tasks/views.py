from requests import request
from accounts.models import User
from .models import Task
from .forms import TaskForm, ProfileForm   
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,TokenError,AccessToken
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login, logout

def home(request):
    return render(request, 'tasks/home.html')

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@csrf_exempt
def jwt_login_page(request):
    username = request.POST.get("username") or ""
    password = request.POST.get("password") or ""
    if request.method == "POST":
        if not username or not password:
                messages.error(request, "Username and password cannot be blank.")
                return render(request, 'tasks/login.html')
    
    user = authenticate(request, username=username, password=password)

    if user is not None and not user.is_staff:
        tokens = get_tokens_for_user(user)
        response = redirect("profile") # Redirect to profile page after login
        response.set_cookie("access_token", tokens["access"], httponly=True)
        response.set_cookie("refresh_token", tokens["refresh"], httponly=True)
        return response
    else:
        if request.method == "POST":
            messages.error(request, "Invalid credentials or admin user.")
        return render(request, 'tasks/login.html')
    

def jwt_logout_page(request):
    try: 
        response = redirect("login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except KeyError:
        messages.error(request, "Refresh token required.")
        return redirect("login")
    except TokenError:
        messages.error(request, "Invalid or expired token")
        return redirect("login")

# @login_required(login_url='/login/')

def task_list(request):
    token = request.COOKIES.get("access_token")
    if not token:
        messages.error(request, "Incorrect credentials.")
        return redirect("login")
    access_token = AccessToken(token)
    user_id = access_token["user_id"]
    tasks = Task.objects.filter(assigned_to=user_id)
    completed_tasks = Task.objects.filter(completed=True,assigned_to=user_id)
    in_progress_tasks = Task.objects.filter(completed=False,assigned_to=user_id)
    return render(request, "tasks/task_list.html", {"tasks": tasks,"completed_tasks": completed_tasks, "in_progress_tasks": in_progress_tasks})

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

def dashboard(request):
    token = request.COOKIES.get("access_token")
    if not token:
        messages.error(request, "Please Login to continue.")
        return redirect("login")
    return render(request, 'tasks/dashboard.html')

def profile(request):
    token = request.COOKIES.get("access_token")
    if not token:
        messages.error(request, "Access token required.")
        return redirect("login") 
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        user = User.objects.get(id=user_id)
    except Exception:
        return redirect("login")

    return render(request, "tasks/profile.html", {"user": user})   

def update_profile(request, pk):
    user = get_object_or_404(User, pk=pk)   # fetch user by primary key
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return render(request, "tasks/profile.html", {"form": form, "user": user})
    else:
        form = ProfileForm(instance=user)
    return render(request, "tasks/profile_form.html", {"form": form})

## This view returns JSON response of all tasks
def user_tasks_json(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    access_token = AccessToken(token)
    user_id = access_token["user_id"]
    tasks = Task.objects.filter(assigned_to=user_id).values("id", "title", "due_date", "completed")
    return JsonResponse(list(tasks), safe=False)
