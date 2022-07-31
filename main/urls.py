from django.urls import path
from . import views

urlpatterns = [
    path('change_log', views.GetChangeLog.as_view(), name='mainGetChangeLog'),
    path('search_for', views.search_system, name='mainSearchDefault'),
    path('search_for/<str:search_term>', views.search_system, name='mainSearchSpecific'),
]