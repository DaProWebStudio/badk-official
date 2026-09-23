from functools import lru_cache

from django import template
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

ICONS_DIR = settings.BASE_DIR / 'templates' / 'icons'


@lru_cache(maxsize=None)
def _read_icon(name):
    return (ICONS_DIR / f'{name}.svg').read_text(encoding='utf-8').strip()


@register.simple_tag
def icon(name, css_class='size-5', stroke_width=2):
    """Инлайн SVG-иконка: {% icon 'arrow-right' 'size-4' %}. Бренды — с префиксом brand-."""
    inner = mark_safe(_read_icon(name))
    if name.startswith('brand-'):
        return format_html(
            '<svg class="{}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{}</svg>',
            css_class, inner,
        )
    return format_html(
        '<svg class="{}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{}" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>',
        css_class, stroke_width, inner,
    )
