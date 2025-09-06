from django import forms
from .models import Task, User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter task title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter task description",
                "rows": 3,
                "style": "resize:none;"
            }),
            "completed": forms.CheckboxInput(attrs={
                "class": "form-check-input",
                "role": "switch"
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email","phone","profile_picture"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }