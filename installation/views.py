from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Installation
from .forms import ViewInstallationForm


# Create your views here.
class AllInstallations(LoginRequiredMixin, generic.ListView):
    model = Installation
    queryset = Installation.objects.all()
    template_name = 'installation/all_installations.html'


class ViewInstallation(LoginRequiredMixin, generic.UpdateView):
    model = Installation
    form_class = ViewInstallationForm
    template_name = 'installation/view_installation.html'
