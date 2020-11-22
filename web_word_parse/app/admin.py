from django.contrib import admin
from .models import Task, Result

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("address", "word", "timestamp", "http_status_code", "task_status")

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("address", "words_count", "http_status_code")