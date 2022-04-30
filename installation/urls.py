from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllInstallations.as_view(), name='allInstallations'),
    path('view/<int:pk>', views.ViewInstallation.as_view(), name='viewInstallation'),
]