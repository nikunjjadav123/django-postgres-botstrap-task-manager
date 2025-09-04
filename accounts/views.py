from django.shortcuts import render
from django.contrib.admin.models import LogEntry

def admin_audit_logs(request):
    logs = LogEntry.objects.select_related("user", "content_type").order_by("-action_time")[:50]
    return render(request, "accounts/admin_audit_logs.html", {"logs": logs})

