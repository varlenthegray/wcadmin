from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmailHomepage.as_view(), name='emailHomepage'),
]