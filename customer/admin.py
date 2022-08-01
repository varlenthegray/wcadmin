from django.contrib import admin
from . import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'quickbooks_id', 'company', 'first_name', 'last_name', 'email', 'main_phone']
    list_display_links = ['id', 'quickbooks_id', 'company', 'first_name', 'last_name']


class CustomerNotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'timestamp', 'created_by']
    list_display_links = ['id', 'subject']
    list_filter = ('system_note',)


class JobSiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'quickbooks_id', 'print_on_check_name', 'email', 'phone_number']
    list_filter = ('active', 'requires_supporting_technician', 'service_scheduled', 'disable_service')
    list_display_links = ['id', 'quickbooks_id', 'print_on_check_name']


class JobSiteEquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_site', 'tags', 'installed_on', 'equipment']
    list_filter = ('equipment',)
    list_display_links = ['id', 'job_site']


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.CustomerNotes, CustomerNotesAdmin)
admin.site.register(models.JobSite, JobSiteAdmin)
admin.site.register(models.JobSiteEquipment, JobSiteEquipmentAdmin)
