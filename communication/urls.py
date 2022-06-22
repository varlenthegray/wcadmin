from django.urls import path
from . import views

urlpatterns = [
    path('compose_email', views.EmailHomepage.as_view(), name='emailCompose'),
    path('all_templates', views.AllTemplates.as_view(), name='emailAllTemplates'),
]