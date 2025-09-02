from django.core.management.base import BaseCommand
from django.utils.timezone import now

from tasks.models import Task


class Command(BaseCommand):
    help = "Update overdue tasks priority"

    def handle(self, *args, **kwargs):
        today = now().date()
        Task.objects.filter(due_date__lt=today).update(priority='High')
        Task.objects.filter(due_date=today).update(priority='Medium')
