from django.urls import path
from . import views

urlpatterns = [
    path('', views.QBDashboard.as_view(), name='qbDashboard')
]