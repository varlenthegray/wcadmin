from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('change_log', views.GetChangeLog.as_view(), name='mainGetChangeLog')
]