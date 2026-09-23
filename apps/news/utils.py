from math import ceil

from django.utils.html import strip_tags

WORDS_PER_MINUTE = 180


def article_context(item, model):
    """Время чтения и другие материалы того же раздела для детальной страницы."""
    words = len(strip_tags(item.description or '').split())
    return {
        'read_minutes': max(1, ceil(words / WORDS_PER_MINUTE)),
        'others': model.active.exclude(pk=item.pk)[:3],
        'gallery': list(item.images.all()),
    }

