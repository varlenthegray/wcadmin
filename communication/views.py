from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EmailHistory
from .forms import CreateEmail


class EmailHomepage(LoginRequiredMixin, generic.CreateView):
    model = EmailHistory
    template_name = 'communication/index.html'
    form_class = CreateEmail
