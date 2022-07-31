from django.contrib import admin
from . import models


class VersionLogAdmin(admin.ModelAdmin):
    list_display = ['version', 'when']


admin.site.register(models.VersionLog, VersionLogAdmin)
