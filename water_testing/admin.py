from django.contrib import admin
from . import models


class WaterTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sample_date', 'sample_address', 'sample_point', 'job_site']
    list_display_links = ['id', 'name']


class LineItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'analyte', 'minimum_limit', 'maximum_limit', 'unit', 'group', 'last_modified_by']
    list_filter = ('unit', 'analyte')
    list_display_links = ['id', 'analyte']


class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on']
    list_display_links = ['id', 'name']


class LineResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'line_item', 'result', 'water_test', 'added_by']
    list_filter = ('line_item',)
    list_display_links = ['id', 'line_item']


class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


admin.site.register(models.WaterTest, WaterTestAdmin)
admin.site.register(models.LineItem, LineItemAdmin)
admin.site.register(models.Template, TemplateAdmin)
admin.site.register(models.LineResult, LineResultAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
