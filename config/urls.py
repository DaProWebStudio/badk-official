from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from services.seo.urls import urlpatterns as seo_urlpatterns

urlpatterns = [
    path('', include(seo_urlpatterns)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
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
    urlpatterns += (
        static(settings.STATIC_URL, document_root=settings.STATIC_DIR) +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
    import debug_toolbar
    urlpatterns += i18n_patterns(path('__debug__/', include(debug_toolbar.urls)), )

