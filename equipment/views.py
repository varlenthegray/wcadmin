from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Equipment
from .forms import AddEquipmentForm


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
