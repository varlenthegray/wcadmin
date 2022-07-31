from django.contrib import admin
from . import models


class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'status', 'user', 'timestamp']
    list_display_links = ['id', 'subject']


admin.site.register(models.EmailHistory, EmailHistoryAdmin)
admin.site.register(models.EmailTemplates)
