from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models
from accounts.models import User


PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date is None:
            return False
        due_datetime = datetime.combine(self.due_date, datetime.min.time(), tzinfo=timezone.get_current_timezone())
        return not self.completed and due_datetime < timezone.now()
    
