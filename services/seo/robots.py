from django.views.decorators.http import require_GET
from django.http import HttpResponse


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /login/",
        "Host: https://badk.kg",
        "Sitemap: https://badk.kg/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
