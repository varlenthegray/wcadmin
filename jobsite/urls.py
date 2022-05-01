from django.urls import path
from . import views

urlpatterns = [
    path('all_job_sites', views.AllJobSites.as_view(), name='allJobSites'),
    path('view/<int:pk>', views.ViewJobSite.as_view(), name='viewJobSite'),
    path('add_job_site', views.AddJobSite.as_view(), name='addJobSite'),
]