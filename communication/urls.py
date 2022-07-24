from django.urls import path
from . import views

urlpatterns = [
    path('compose_email', views.EmailHomepage.as_view(), name='emailCompose'),
    path('get_template/<int:pk>', views.get_existing_template, name='getTemplate'),
    path('all_templates', views.AllTemplates.as_view(), name='emailAllTemplates'),
    path('create_new_template', views.CreateNewTemplate.as_view(), name='createNewTemplate'),
    path('edit_template/<int:pk>', views.EditTemplate.as_view(), name='emailEditTemplate'),
    path('delete_template/<int:pk>', views.delete_template, name='deleteEmailTemplate'),
    path('sent_mail', views.AllSentMail.as_view(), name='emailSentMail'),
    path('drafts', views.AllDrafts.as_view(), name='emailDrafts'),
    path('view_draft/<int:pk>', views.ViewDraft.as_view(), name='viewEmailDraft'),
    path('get_email_history/<int:pk>', views.get_email_history, name='getEmailHistory'),
]