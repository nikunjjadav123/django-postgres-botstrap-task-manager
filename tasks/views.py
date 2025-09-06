import calendar
from datetime import datetime
from requests import request
from accounts.models import User
from .models import Task
from .forms import TaskForm, ProfileForm   
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,TokenError,AccessToken
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash


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
        response = redirect("dashboard") # Redirect to dashboard after login
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
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        user = User.objects.get(id=user_id)
    except Exception:
        return redirect("login")
    
    now = datetime.now()
    year = now.year
    month = now.month
    cal = HighlightCalendar(today=now, firstweekday=calendar.SUNDAY)
    calendar_html = cal.formatmonth(year, month)
    return render(request, 'tasks/dashboard.html', {"user": user, "calendar_html": calendar_html})

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
    token = request.COOKIES.get("access_token")
    access_token = AccessToken(token)
    user_id = access_token["user_id"]
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "tasks/profile_form.html", {"form": form})

def change_password(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        token = request.COOKIES.get("access_token")
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        get_user = User.objects.get(id=user_id)
      
        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        user = authenticate(request, username=get_user.username, password=current_password)

        if user is None:
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("change_password")
        
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "✅ Password changed successfully!")
        return redirect("change_password")

    return render(request, "tasks/change_password.html")

## This view returns JSON response of all tasks
def user_tasks_json(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    access_token = AccessToken(token)
    user_id = access_token["user_id"]
    tasks = Task.objects.filter(assigned_to=user_id).values("id", "title", "due_date", "completed")
    return JsonResponse(list(tasks), safe=False)


## Calendar class to highlight current date
class HighlightCalendar(calendar.HTMLCalendar):
    def __init__(self, today, firstweekday=0):
        super().__init__(firstweekday)
        self.today = today

    def formatday(self, day, weekday):
        if day == 0:  # padding days
            return '<td class="noday">&nbsp;</td>'
        if day == self.today.day and self.today.month == self.today.month and self.today.year == self.today.year:
            # Highlight today
            return f'<td class="today bg-warning fw-bold">{day}</td>'
        return f'<td class="{self.cssclasses[weekday]}">{day}</td>'
