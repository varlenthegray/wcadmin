from django.urls import path
from . import views

urlpatterns = [
    path('all_equipment', views.AllEquipment.as_view(), name='allEquipment'),
    path('add_equipment', views.AddEquipment.as_view(), name='addEquipment'),
    path('view_equipment/<int:pk>', views.ViewEquipment.as_view(), name='viewEquipment'),
]