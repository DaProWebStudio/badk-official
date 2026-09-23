from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from services.seo.urls import urlpatterns as seo_urlpatterns

urlpatterns = [
    path('', include(seo_urlpatterns)),
    path('rosetta/', include('rosetta.urls')),
    # Загруженные файлы отдаёт сам Django: отдельного nginx для /media/ на сервере нет
    re_path(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('specialties/', include('apps.specialty.urls')),
    path('contacts/', include('apps.feedback.urls')),
    path('employee/', include('apps.employee.urls')),
    path('students/', include('apps.student.urls')),
    path('news/', include('apps.news.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
    import debug_toolbar
    urlpatterns += i18n_patterns(path('__debug__/', include(debug_toolbar.urls)), )

