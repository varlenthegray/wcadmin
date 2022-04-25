from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllCustomers.as_view(), name='allCustomers'),
    path('add/', views.AddCustomer.as_view(), name='addCustomer'),
    path('view/<int:pk>', views.ViewCustomer.as_view(), name='viewCustomer'),
    path('report/this_month', views.CustomersDueThisMonth.as_view(), name='customersDueThisMonth'),
    path('report/next_month', views.CustomersDueNextMonth.as_view(), name='customersDueNextMonth'),
    path('report/two_months_future', views.CustomersDueTwoMonthsFuture.as_view(), name='customerDueTwoMonthsFuture'),
    path('report/last_month', views.CustomersDueLastMonth.as_view(), name='customerDueLastMonth'),
    path('report/last_three_months', views.CustomersDueLastThreeMonths.as_view(), name='customerDueLastThreeMonths'),
    path('report/custom_report', views.CustomersCustomReport.as_view(), name='customerCustomReport')
]
