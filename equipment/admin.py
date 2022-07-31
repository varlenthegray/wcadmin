from django.contrib import admin
from . import models


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['quickbooks_id', 'sku', 'name', 'cost', 'is_active', 'created_on']


admin.site.register(models.Equipment, EquipmentAdmin)
