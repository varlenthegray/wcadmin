from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.CustomerEquipment)
admin.site.register(models.CustomerNotesCategory)
admin.site.register(models.CustomerNotes)
admin.site.register(models.CustomerEquipmentPhotos)
