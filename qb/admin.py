from django.contrib import admin
from .models import Invoice, InvoiceLine, QBSystem


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_num', 'job_site', 'invoice_date', 'total', 'memo', 'service_interval')
    list_filter = ('service_interval',)
    list_display_links = ('id', 'invoice_num', 'job_site')


class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'description', 'price', 'quantity')
    list_display_links = ('id', 'invoice')


class QBSystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_update', 'user_id')
    list_display_links = ('id', 'last_update')


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceLine, InvoiceLineAdmin)
admin.site.register(QBSystem, QBSystemAdmin)
