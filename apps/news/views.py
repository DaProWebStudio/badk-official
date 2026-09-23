from django.db.models import Prefetch
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.news.models import News, NewsImages
from apps.news.utils import article_context


class NewsListView(ListView):
    model = News
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
        context['title'] = _('Новости')
        context['sub_title'] = _('Новости колледжа')
        context['query'] = self.request.GET.get('q', '').strip()
        return context


class NewsDetailView(DetailView):
    model = News
    queryset = model.active.prefetch_related(
        Prefetch('images', NewsImages.objects.only('image'))
    )
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Новости')
        context.update(article_context(self.object, News))
        return context
