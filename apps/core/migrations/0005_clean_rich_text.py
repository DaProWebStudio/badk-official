"""
Чистка HTML, оставшегося от CKEditor, тем же санитайзером, что и в prose-editor.

Убирает стили и шрифты, вставленные из Word (span style=..., font-family, text-indent),
превращает div в абзацы и удаляет пустые абзацы. Текст, жирный, курсив, списки
и ссылки сохраняются.
"""
import re

from django.db import migrations

from common.richtext import RICH_TEXT_EXTENSIONS

# (app_label, model, базовое поле) — вместе с переводами *_ru/_ky/_en
RICH_FIELDS = [
    ('news', 'News', 'description'),
    ('student', 'StudentLive', 'description'),
    ('student', 'StudentCouncil', 'description'),
    ('specialty', 'Specialty', 'description'),
    ('employee', 'Employee', 'description'),
    ('core', 'InternationalCooperation', 'description'),
    ('core', 'SiteContent', 'value'),
]

EMPTY_PARAGRAPH = re.compile(r'<p>(?:\s|&nbsp;|\xa0|<br\s*/?>)*</p>')


def clean(html, sanitize):
    if not html:
        return html
    html = re.sub(r'<div\b[^>]*>', '<p>', html, flags=re.I)
    html = re.sub(r'</div\s*>', '</p>', html, flags=re.I)
    html = sanitize(html)
    html = EMPTY_PARAGRAPH.sub('', html)
    return html.strip()


def forwards(apps, schema_editor):
    from django_prose_editor.fields import create_sanitizer

    sanitize = create_sanitizer(RICH_TEXT_EXTENSIONS)

    for app_label, model_name, base in RICH_FIELDS:
        model = apps.get_model(app_label, model_name)
        names = [
            f.name for f in model._meta.concrete_fields
            if f.name == base or f.name in (f'{base}_ru', f'{base}_ky', f'{base}_en')
        ]
        for obj in model.objects.only('pk', *names).iterator():
            changed = {}
            for name in names:
                value = getattr(obj, name)
                cleaned = clean(value, sanitize)
                if cleaned != value:
                    changed[name] = cleaned
            if changed:
                model.objects.filter(pk=obj.pk).update(**changed)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_sitecontent_en_ky'),
        ('news', '0001_initial'),
        ('student', '0001_initial'),
        ('specialty', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
