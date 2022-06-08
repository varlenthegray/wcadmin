from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import JobSite
from .forms import ViewJobSiteForm


# Create your views here.
class AllJobSites(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.all().prefetch_related('customer')
    template_name = 'jobsite/all_jobsites.html'


class ViewJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    form_class = ViewJobSiteForm
    template_name = 'jobsite/view_jobsite.html'


class AddJobSite(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    form_class = ViewJobSiteForm
    template_name = 'jobsite/add_jobsite.html'
