from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import StudentCouncil, StudentLive, StudentLiveImages


class StudentCouncilView(ListView):
    model = StudentCouncil
    queryset = model.active.all()
    context_object_name = 'students'
    template_name = 'student/index.html'


class StudentDetailView(DetailView):
    model = StudentCouncil
    queryset = model.active.all()
    slug_field = 'slug'
    context_object_name = 'student'
    template_name = 'student/student_detail.html'


class StudentLiveListView(ListView):
    model = StudentLive
    queryset = model.active.all()
    context_object_name = 'news'
    template_name = 'news/list.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Студенческая жизнь')
        context['sub_title'] = _('Студентам')
        context['query'] = self.request.GET.get('q', '').strip()
        return context


class StudentLiveDetailView(DetailView):
    model = StudentLive
    queryset = model.active.prefetch_related(
        Prefetch('images', StudentLiveImages.objects.only('image'))
    )
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Студенческая жизнь')
        return context
