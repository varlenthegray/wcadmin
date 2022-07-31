from django.contrib import admin
from . import models


class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'status', 'user', 'timestamp']


admin.site.register(models.EmailHistory, EmailHistoryAdmin)
admin.site.register(models.EmailTemplates)
