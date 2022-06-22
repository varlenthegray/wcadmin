from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EmailHistory, EmailTemplates
from .forms import CreateEmail
from jobsite.models import JobSite


class EmailHomepage(LoginRequiredMixin, generic.CreateView):
    model = EmailHistory
    template_name = 'communication/compose_email.html'
    form_class = CreateEmail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        return context


class AllTemplates(LoginRequiredMixin, generic.ListView):
    model = EmailTemplates
    template_name = 'communication/all_templates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        return context


class AllSentMail(LoginRequiredMixin, generic.ListView):
    model = EmailHistory
    template_name = 'communication/all_sent_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        return context


class AllDrafts(LoginRequiredMixin, generic.ListView):
    model = EmailHistory
    template_name = 'communication/drafts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['email_drafts'] = EmailHistory.objects.filter(status='draft')
        return context


class AllTrash(LoginRequiredMixin, generic.ListView):
    model = EmailHistory
    template_name = 'communication/trash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['all_trash'] = EmailHistory.objects.filter(status='deleted')
        return context
