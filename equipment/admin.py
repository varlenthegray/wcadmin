from django.contrib import admin
from . import models


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['quickbooks_id', 'sku', 'name', 'cost', 'is_active', 'created_on']
    list_display_links = ['sku', 'name']


admin.site.register(models.Equipment, EquipmentAdmin)
