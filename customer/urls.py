from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'allJobSitesRest', views.JobSitesREST)

urlpatterns = [
    path('add_customer', views.AddCustomer.as_view(), name='addCustomer'),
    path('save_customer', views.SaveCustomer.as_view(), name='saveCustomer'),
    path('save_notes', views.SaveNoteToCustomer.as_view(), name='saveCustomerNotes'),

    path('add/job_site', views.AddJobSiteToCustomer.as_view(), name='addJobSiteToCustomer'),
    path('save/job_site', views.SaveJobSiteToCustomer.as_view(), name='saveJobSiteToCustomer'),
    path('view/job_site/<int:pk>', views.ViewSpecificJobSite.as_view(), name='viewSpecificJobSite'),
    path('update/job_site/<int:pk>', views.UpdateJobSite.as_view(), name='updateJobSite'),

    path('view/job_site/edit_equipment/<int:pk>', views.ViewEditEquipmentLine.as_view(), name='viewEditEquipmentLine'),
    path('view/job_site/save_equipment/<int:pk>', views.SaveEquipmentChanges.as_view(), name='saveEquipmentChanges'),
    path('view/job_site/add_equipment', views.AddEquipmentToJobSite.as_view(), name='addJobSiteEquipment'),
    path('view/job_site/delete_equipment/<int:pk>', views.ViewDeleteEquipmentFromJobSite.as_view(),
         name='viewJobSiteDeleteEquipment'),

    path('reports/due_this_month', views.CustomersDueThisMonth.as_view(), name='customersDueThisMonth'),
    path('reports/due_next_month', views.CustomersDueNextMonth.as_view(), name='customersDueNextMonth'),
    path('reports/two_months_future', views.CustomersDueTwoMonthsFuture.as_view(), name='customerDueTwoMonthsFuture'),
    path('report/last_month', views.CustomersDueLastMonth.as_view(), name='customerDueLastMonth'),
    path('report/last_three_months', views.CustomersDueLastThreeMonths.as_view(), name='customerDueLastThreeMonths'),
    path('report/custom_report', views.CustomersCustomReport.as_view(), name='customerCustomReport'),
    path('report/last_year_this_month', views.CustomersDueLastYearThisMonth.as_view(),
         name='customerDueLastYearThisMonth'),

    path('all_job_sites', views.AllJobSites.as_view(), name='allJobSites'),
    path('view/<int:pk>', views.ViewJobSite.as_view(), name='viewJobSite'),
    path('add_job_site', views.AddJobSite.as_view(), name='addJobSite'),
    path('all_job_sites_json', views.all_job_sites_json, name='allJobSitesJSON'),
    # path('print_address_labels', views.PrintAddressLabels.as_view(), name='printAddrLabels'),
    path('print_address_labels', views.print_address_labels, name='printAddrLabels'),
    path('set_job_scheduled/<int:pk>', views.set_job_site_scheduled, name='setJobSiteScheduled'),
    re_path('^api/', include(router.urls)),
]
