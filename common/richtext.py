from django_prose_editor.fields import ProseEditorField

# Что можно делать в редакторе. Санитайзер (nh3) пропускает в базу только эти теги,
# поэтому стили и шрифты, вставленные из Word, вычищаются при сохранении.
RICH_TEXT_EXTENSIONS = {
    'Bold': True,
    'Italic': True,
    'Underline': True,
    'Strike': True,
    'Heading': {'levels': [2, 3]},
    'BulletList': True,
    'OrderedList': True,
    'ListItem': True,
    'Blockquote': True,
    'HorizontalRule': True,
    'HardBreak': True,
    'Link': {'enableTarget': True, 'protocols': ['http', 'https', 'mailto', 'tel']},
    'Table': True,
    'TableRow': True,
    'TableHeader': True,
    'TableCell': True,
    'Typographic': True,
}


def RichTextField(*args, **kwargs):
    """HTML-поле с редактором prose-editor. В базе — обычный TextField."""
    return ProseEditorField(*args, extensions=dict(RICH_TEXT_EXTENSIONS), sanitize=True, **kwargs)
