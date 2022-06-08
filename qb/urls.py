from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='qbDashboard'),
    path('oauth/', views.oauth, name='oauth'),
    path('callback/', views.callback, name='callback'),
    path('connected/', views.connected, name='connected'),
    path('qbo_request/', views.qbo_request, name='qbo_request'),
    path('revoke/', views.revoke, name='revoke'),
    path('refresh/', views.refresh, name='refresh'),
    path('user_info/', views.user_info, name='user_info'),
    path('get_customers/', views.get_qb_customers, name='get_qb_customers'),
    path('insert_customers_db/', views.insert_qb_customers, name='insert_qb_customers'),
    path('get_service_data/', views.get_service_data, name='get_qb_service_data'),
    path('calculate_service_date/', views.calculate_service_date, name='calculate_service_date'),
    path('get_equipment/', views.get_equipment_qb, name='get_qb_equipment'),
]