import logging
import markdown
import simplejson

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect

from .models import EmailHistory, EmailTemplates
from .forms import CreateEmail, CreateTemplate
from customer.models import Customer, CustomerNotes, JobSite

logger = logging.getLogger(__name__)


class EmailHomepage(LoginRequiredMixin, generic.CreateView):
    model = EmailHistory
    template_name = 'communication/compose_email.html'
    form_class = CreateEmail
    success_url = '?sent=true'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        context['existing_templates'] = EmailTemplates.objects.all()
        return context

    def form_valid(self, form):
        form_save = form.save(commit=False)
        form_save.user = self.request.user
        draft = self.request.GET.get('draft')

        cc_form_value = form.cleaned_data.get('send_cc')
        bcc_form_value = form.cleaned_data.get('send_bcc')

        if draft:
            form_save.status = 'draft'
        else:
            form_save.status = 'sent'

            send_cc = []

            for user in cc_form_value:
                send_cc.append(user.email)

            for customer in bcc_form_value:
                note = CustomerNotes(
                    subject="Email Sent",
                    note="An email was sent to this customer.",
                    created_by=self.request.user,
                    customer=customer
                )

                note.save()

                job_site_record = JobSite.objects.get(customer=customer)

                message_raw = form.cleaned_data.get('message')
                message_output = message_raw.replace('{{customer.first_name}}', customer.first_name)
                message_output = message_output.replace('{{customer.last_name}}', customer.last_name)
                message_output = message_output.replace('{{customer.last_name}}', customer.last_name)
                message_output = message_output.replace('{{customer.company}}', customer.company)
                message_output = message_output.replace('{{jobsite.print_on_check_name}}',
                                                        job_site_record.print_on_check_name)
                message_output = message_output.replace('{{customer.email}}', customer.email)
                message_output = message_output.replace('{{jobsite.name}}', job_site_record.name)

                if job_site_record.next_service_date:
                    message_output = message_output.replace('{{jobsite.next_service_date}}',
                                                            job_site_record.next_service_date.strftime("%b %d, %Y"))
                else:
                    message_output = message_output.replace('{{jobsite.next_service_date}}', "Not Scheduled")

                message = EmailMultiAlternatives(
                    subject=form.cleaned_data.get('subject'),
                    body=message_output,
                    from_email='info@wcwater.com',
                    to=[customer.email],
                    cc=send_cc,
                )

                message.attach_alternative(markdown.markdown(message_output), 'text/html')

                message.send(fail_silently=False)

                form.message = message_output

        form.save()

        if not draft:
            return super().form_valid(form)
        else:
            return HttpResponseRedirect('?save_draft=true')

    def form_invalid(self, form):
        bcc_form = form

        if self.request.POST.get('data'):
            # fancy footwork to get POST data and represent it as an array, then get objects from the array
            raw_job_site_ids = simplejson.loads(self.request.POST.get('data'))['body']
            job_site_ids = []

            # this has to be done, it's a 3D array initially with 1 array, [0] didn't work
            for js_id in raw_job_site_ids:
                job_site_ids.append(js_id[0])

            bcc_form = CreateEmail(initial={'send_bcc': Customer.objects.filter(jobsite__in=job_site_ids)
                                   .exclude(email=None).order_by('first_name', 'last_name', 'company', 'email')})

        response = super().form_invalid(bcc_form)

        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)


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


class ViewSentEmail(LoginRequiredMixin, generic.DetailView):
    model = EmailHistory
    template_name = 'communication/modal/view_sent_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_email'] = EmailHistory.objects.prefetch_related('send_bcc', 'send_cc__send_cc').get(
            pk=self.object.pk)

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
    form_class = CreateEmail
    success_url = '/email/drafts?sent=true'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = JobSite.objects.filter(active=True).exclude(email=None)
        return context

    def form_invalid(self, form):
        response = super().form_invalid(form)

        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        form_save = form.save(commit=False)
        form_save.user = self.request.user
        draft = self.request.GET.get('draft')

        if draft:
            form_save.status = 'draft'
        else:
            form_save.status = 'sent'

            send_cc = []

            for user in form.cleaned_data.get('send_cc'):
                send_cc.append(user.email)

            for customer in form.cleaned_data.get('send_bcc'):
                note = CustomerNotes(
                    subject="Email Sent",
                    note="An email was sent to this customer.",
                    created_by=self.request.user,
                    customer=customer
                )

                note.save()

                job_site_record = JobSite.objects.get(customer=customer)

                message_raw = form.cleaned_data.get('message')
                message_output = message_raw.replace('{{customer.first_name}}', customer.first_name)
                message_output = message_output.replace('{{customer.last_name}}', customer.last_name)
                message_output = message_output.replace('{{customer.last_name}}', customer.last_name)
                message_output = message_output.replace('{{customer.company}}', customer.company)
                message_output = message_output.replace('{{jobsite.print_on_check_name}}',
                                                        job_site_record.print_on_check_name)
                message_output = message_output.replace('{{customer.email}}', customer.email)
                message_output = message_output.replace('{{jobsite.name}}', job_site_record.name)

                if job_site_record.next_service_date:
                    message_output = message_output.replace('{{jobsite.next_service_date}}',
                                                            job_site_record.next_service_date.strftime("%b %d, %Y"))
                else:
                    message_output = message_output.replace('{{jobsite.next_service_date}}', "Not Scheduled")

                message = EmailMultiAlternatives(
                    subject=form.cleaned_data.get('subject'),
                    body=message_output,
                    from_email='info@wcwater.com',
                    to=[customer.email],
                    cc=send_cc,
                )

                message.attach_alternative(markdown.markdown(message_output), 'text/html')

                message.send(fail_silently=False)

                form.message = message_output

        form.save()

        if not draft:
            return super().form_valid(form)
        else:
            response = redirect('emailDrafts')
            response['Location'] += '?save_draft=true'

            return response
