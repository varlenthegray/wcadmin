from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import VersionLog


class GetChangeLog(LoginRequiredMixin, generic.ListView):
    model = VersionLog
    queryset = VersionLog.objects.all()
    template_name = 'main/change_log.html'
