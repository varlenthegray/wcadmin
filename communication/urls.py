from django.urls import path
from . import views

urlpatterns = [
    path('compose_email', views.EmailHomepage.as_view(), name='emailCompose'),
    path('all_templates', views.AllTemplates.as_view(), name='emailAllTemplates'),
    path('edit_template/<int:pk>', views.EditTemplate.as_view(), name='emailEditTemplate'),
    path('sent_mail', views.AllSentMail.as_view(), name='emailSentMail'),
    path('drafts', views.AllDrafts.as_view(), name='emailDrafts'),
    path('trash', views.AllTrash.as_view(), name='emailTrash'),
]