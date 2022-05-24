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
]