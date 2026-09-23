from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.specialty.models import Specialty


class SpecialtyListView(ListView):
    model = Specialty
    queryset = model.active.all()
    context_object_name = 'specialties'
    template_name = 'specialty/list.html'


class SpecialtyDetailView(DetailView):
    model = Specialty
    queryset = model.active.all()
    context_object_name = 'specialty'
    template_name = 'specialty/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['others'] = Specialty.active.exclude(pk=self.object.pk)[:3]
        return context
