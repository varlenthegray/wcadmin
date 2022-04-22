from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllCustomers.as_view(), name='allCustomers'),
    path('add/', views.AddCustomer.as_view(), name='addCustomer')
]
