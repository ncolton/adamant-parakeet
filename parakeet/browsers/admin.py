from django.contrib import admin

from .models import Browser


class BrowserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Browser, BrowserAdmin)
