from django.contrib import admin

from .models import JobConfiguration


@admin.register(JobConfiguration)
class JobConfigurationAdmin(admin.ModelAdmin):
    list_display = ('enabled', 'partner', 'scheduling_interval')
