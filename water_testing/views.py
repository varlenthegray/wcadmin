from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import WaterTest, LineResult


class ViewAllWaterTests(LoginRequiredMixin, generic.ListView):
    model = WaterTest
    template_name = 'water_testing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewWaterReport(LoginRequiredMixin, generic.DetailView):
    model = WaterTest
    template_name = 'water_testing/water_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['line_results'] = LineResult.objects.filter(water_test=self.object.pk)\
            .order_by('line_item__group', '-line_item__lineresult__result')
        return context
