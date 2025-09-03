from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.html import linebreaks
from .models import Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'formatted_description', 'completed', 'created_at')
    list_filter = ('completed',)
    search_fields = ('title', 'description')

    def formatted_description(self, obj):
        return mark_safe(linebreaks(obj.description))

    formatted_description.short_description = "Task Description"