"""wcadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('customers/', include('customer.urls'), name='customers'),
    path('users/', include('users.urls'), name='users'),
    path('job_sites/', include('customer.urls'), name='jobsite'),
    path('equipment/', include('equipment.urls'), name='equipment'),
    path('qb/', include('qb.urls'), name='qb'),
    path('email/', include('communication.urls'), name='email'),
    path('main/', include('main.urls'), name='main'),
    path('water_test/', include('water_testing.urls'), name='water_test'),
]
