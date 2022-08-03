from django.urls import path
from . import views

urlpatterns = [
    path('all_test_results', views.ViewAllWaterTests.as_view(), name='viewAllWaterTests'),
    path('view_results/<int:pk>', views.ViewWaterReport.as_view(), name='viewWaterReport'),
]