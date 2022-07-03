from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from .models import Equipment
from .forms import AddEquipmentForm

from jobsite.models import JobSiteEquipment


class AllEquipment(LoginRequiredMixin, generic.ListView):
    template_name = 'equipment/all_equipment.html'
    model = Equipment
    queryset = Equipment.objects.all()


class AddEquipment(LoginRequiredMixin, generic.CreateView):
    template_name = 'equipment/add_equipment.html'
    model = Equipment
    form_class = AddEquipmentForm

    def post(self, request, *args, **kwargs):
        create_equipment = AddEquipmentForm(request.POST)

        if create_equipment.is_valid():
            data = create_equipment.save(commit=False)
            data.last_updated_by = request.user
            data.save()

            return HttpResponseRedirect(reverse('allEquipment') + "?submitted=True")
        else:
            return HttpResponseBadRequest('invalid')


class ViewEquipment(LoginRequiredMixin, generic.UpdateView):
    template_name = 'equipment/view_equipment.html'
    model = Equipment
    form_class = AddEquipmentForm

    def post(self, request, *args, **kwargs):
        equipment = Equipment.objects.get(pk=self.kwargs['pk'])
        update_equipment = AddEquipmentForm(request.POST, instance=equipment)

        if update_equipment.is_valid():
            data = update_equipment.save(commit=False)

            data.last_updated_by = request.user
            data.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "?submitted=True")
        else:
            return HttpResponseBadRequest('invalid')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attached_job_sites'] = JobSiteEquipment.objects.filter(equipment=self.object.pk)\
            .select_related('job_site')
        return context
