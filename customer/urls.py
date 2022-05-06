from django.urls import path
from . import views

urlpatterns = [
    path('all_customers', views.AllCustomers.as_view(), name='allCustomers'),
    path('add_customer', views.AddCustomer.as_view(), name='addCustomer'),
    path('view/<int:pk>', views.view_customer, name='viewCustomer'),
    path('view/job_site/<int:pk>', views.ViewSpecificJobSite.as_view(), name='viewSpecificJobSite'),
    path('reports/due_this_month', views.CustomersDueThisMonth.as_view(), name='customersDueThisMonth'),
    path('reports/due_next_month', views.CustomersDueNextMonth.as_view(), name='customersDueNextMonth'),
    path('reports/two_months_future', views.CustomersDueTwoMonthsFuture.as_view(), name='customerDueTwoMonthsFuture'),
    path('report/last_month', views.CustomersDueLastMonth.as_view(), name='customerDueLastMonth'),
    path('report/last_three_months', views.CustomersDueLastThreeMonths.as_view(), name='customerDueLastThreeMonths'),
    path('report/custom_report', views.CustomersCustomReport.as_view(), name='customerCustomReport'),
    path('report/last_year_this_month', views.CustomersDueLastYearThisMonth.as_view(),
         name='customerDueLastYearThisMonth'),
]
