from django.contrib import admin
from .models import Queue

# Register your models here.


@admin.register(Queue)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ["name", "region"]
