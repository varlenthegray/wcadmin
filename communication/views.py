import logging
import markdown

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives

from .models import EmailHistory, EmailTemplates
from .forms import CreateEmail, CreateTemplate

from customer.models import JobSite

logger = logging.getLogger(__name__)


class EmailHomepage(LoginRequiredMixin, generic.CreateView):
    model = EmailHistory
    template_name = 'communication/compose_email.html'
    form_class = CreateEmail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['existing_templates'] = EmailTemplates.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        send_email = CreateEmail(request.POST)

        logger.warning(request.POST.get('send_bcc[]'))

        if send_email.is_valid():
            form_save = send_email.save(commit=False)
            form_save.user = request.user

            if request.GET.get('draft'):
                form_save.status = 'draft'
            else:
                form_save.status = 'sent'

                message = EmailMultiAlternatives(
                    subject=request.POST.get('subject'),
                    body=request.POST.get('message'),
                    from_email='info@wcwater.com',
                    to=['info@wcwater.com'],
                    bcc=[request.POST.get('send_bcc')],
                    cc=[request.POST.get('send_cc')],
                )

                message.attach_alternative(markdown.markdown(request.POST.get('message')), 'text/html')
                # message.send(fail_silently=False)

            form_save.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(send_email.errors)


class AllTemplates(LoginRequiredMixin, generic.CreateView):
    model = EmailTemplates
    template_name = 'communication/all_templates.html'
    form_class = CreateTemplate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['existing_templates'] = EmailTemplates.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        create_template = CreateTemplate(request.POST)

        if create_template.is_valid():
            data = create_template.save(commit=False)
            data.last_updated_by = request.user
            data.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(create_template.errors)


class EditTemplate(LoginRequiredMixin, generic.UpdateView):
    model = EmailTemplates
    template_name = 'communication/modal/edit_template.html'
    form_class = CreateTemplate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['existing_templates'] = EmailTemplates.objects.all()
        context['template_pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        existing_template = EmailTemplates.objects.get(pk=request.POST.get('template_pk'))
        edit_template = CreateTemplate(request.POST, instance=existing_template)

        if edit_template.is_valid():
            data = edit_template.save(commit=False)
            data.last_updated_by = request.user
            data.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(edit_template.errors)


@login_required
def delete_template(request, pk):
    email_template = EmailTemplates.objects.get(pk=pk)
    email_template.delete()

    return HttpResponse(status=200)


@login_required
def get_existing_template(request, pk):
    existing_template = EmailTemplates.objects.filter(pk=pk).values()
    template_list = list(existing_template)

    return JsonResponse(template_list, safe=False)


@login_required
def get_email_history(request, pk):
    existing_email = EmailHistory.objects.filter(pk=pk).values()
    bcc_list = list(existing_email)

    return JsonResponse(bcc_list, safe=False)


class CreateNewTemplate(LoginRequiredMixin, generic.CreateView):
    model = EmailTemplates
    template_name = 'communication/modal/create_new_template.html'
    form_class = CreateTemplate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['existing_templates'] = EmailTemplates.objects.all()
        return context


class AllSentMail(LoginRequiredMixin, generic.ListView):
    model = EmailHistory
    template_name = 'communication/all_sent_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['sent_email'] = EmailHistory.objects.filter(~Q(status='draft'))
        return context


class AllDrafts(LoginRequiredMixin, generic.ListView):
    model = EmailHistory
    template_name = 'communication/drafts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['email_drafts'] = EmailHistory.objects.filter(status='draft')
        return context


class ViewDraft(LoginRequiredMixin, generic.UpdateView):
    model = EmailHistory
    template_name = 'communication/modal/view_draft.html'
    form_class = CreateTemplate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['existing_templates'] = EmailTemplates.objects.all()
        context['email_pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        existing_template = EmailTemplates.objects.get(pk=request.POST.get('template_pk'))
        edit_template = CreateTemplate(request.POST, instance=existing_template)

        if edit_template.is_valid():
            data = edit_template.save(commit=False)
            data.last_updated_by = request.user
            data.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(edit_template.errors)
