from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Equipment
from .forms import AddEquipmentForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse


class AllEquipment(LoginRequiredMixin, generic.ListView):
    template_name = 'equipment/all_equipment.html'
    model = Equipment
    queryset = Equipment.objects.all()


class AddEquipment(LoginRequiredMixin, generic.CreateView):
    template_name = 'equipment/add_equipment.html'
    model = Equipment
    form_class = AddEquipmentForm


class ViewEquipment(LoginRequiredMixin, generic.UpdateView):
    template_name = 'equipment/view_equipment.html'
    model = Equipment
    form_class = AddEquipmentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.parent_id = self.object.pk
            return HttpResponse('success')
        else:
            return HttpResponseBadRequest('invalid')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
