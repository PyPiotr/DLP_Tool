from django.contrib import admin
from dlp_app import models


@admin.register(models.LossPreventionPattern)
class DataLeakAdmin(admin.ModelAdmin):
    list_display = ["description", "pattern"]


@admin.register(models.DataLeak)
class LossPreventionPatternAdmin(admin.ModelAdmin):
    list_display = ["message", "content", "channel", "pattern"]
