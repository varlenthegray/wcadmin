from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'allJobSitesRest', views.JobSitesREST)

urlpatterns = [
    path('all_job_sites', views.AllJobSites.as_view(), name='allJobSites'),
    path('view/<int:pk>', views.ViewJobSite.as_view(), name='viewJobSite'),
    path('add_job_site', views.AddJobSite.as_view(), name='addJobSite'),
    path('all_job_sites_json', views.all_job_sites_json, name='allJobSitesJSON'),
    path('set_job_scheduled/<int:pk>', views.set_job_site_scheduled, name='setJobSiteScheduled'),
    re_path('^api/', include(router.urls)),
]