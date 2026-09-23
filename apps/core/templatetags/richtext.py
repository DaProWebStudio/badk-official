import re

from django import template
from django.template.defaultfilters import linebreaks_filter
from django.utils.safestring import mark_safe

register = template.Library()

_HAS_BLOCK_TAGS = re.compile(r'<(p|div|ul|ol|h[1-6]|table|blockquote)\b', re.I)


@register.filter
def as_paragraphs(value):
    """HTML из редактора выводим как есть, обычный текст — разбиваем на абзацы по переносам."""
    if not value:
        return ''
    if _HAS_BLOCK_TAGS.search(value):
        return mark_safe(value)
    return linebreaks_filter(value, autoescape=False)
