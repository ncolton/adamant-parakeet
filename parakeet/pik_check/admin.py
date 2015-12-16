from django.contrib import admin

import models


@admin.register(models.Browser)
class BrowserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ('code', 'name')


@admin.register(models.JobConfiguration)
class JobConfigurationAdmin(admin.ModelAdmin):
    list_display = ('enabled', 'partner', 'scheduling_interval')
