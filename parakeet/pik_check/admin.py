from django.contrib import admin
from django.utils.timesince import timeuntil

import models


@admin.register(models.Browser)
class BrowserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'active_after', 'inactive_after', 'browsers', 'scheduling_interval']
    list_display = ('code', 'name', 'is_active')


@admin.register(models.ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ('partner', 'browser', 'hold_until', 'time_to_hold_as_string', 'is_on_hold', 'dispatched')

    def time_to_hold_as_string(self, obj):
        return timeuntil(obj.hold_until)


@admin.register(models.CheckStage)
class CheckStageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ordering')
    list_editable = ('ordering',)
