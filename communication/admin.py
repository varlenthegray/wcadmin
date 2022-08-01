from django.contrib import admin
from . import models


class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'status', 'user', 'timestamp']
    list_display_links = ['id', 'subject']
    list_filter = ('status',)


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template_name', 'subject', 'last_updated_on', 'last_updated_by']
    list_display_links = ['id', 'template_name']


admin.site.register(models.EmailHistory, EmailHistoryAdmin)
admin.site.register(models.EmailTemplates, EmailTemplateAdmin)
