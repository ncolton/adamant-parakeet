from django.contrib import admin

from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ('code', 'name')

admin.site.register(Partner, PartnerAdmin)
