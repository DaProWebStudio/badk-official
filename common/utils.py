import re
from random import choice
from urllib.parse import quote

import transliterate

from django.utils.text import slugify


def get_english_translit(text: str, slug: bool = True):
    letters = {'ң': 'н', 'ү': 'y', 'ө': 'о'}
    for key, value in letters.items():
        text = text.replace(key, value)
    try:
        translit = transliterate.translit(text, reversed=True)
    except transliterate.exceptions.LanguageDetectionError:
        translit = text
    return slugify(translit) if slug else translit


def get_random_model(model, exclude_pk=None):
    """Случайная запись модели или None, если записей нет."""
    pks = list(model.objects.exclude(pk=exclude_pk).values_list('pk', flat=True))
    if not pks:
        # Единственная запись — лучше показать её повторно, чем остаться без капчи
        pks = list(model.objects.values_list('pk', flat=True))
    if not pks:
        return None
    return model.objects.get(pk=choice(pks))


def format_phone_number(phone_number):
    numbers = re.findall(r'\d', phone_number)
    if len(numbers) != 12:
        return "Неправильный формат номера телефона"
    return '+{} ({}) {}-{}-{}'.format(
        ''.join(numbers[0:3]),
        ''.join(numbers[3:6]),
        ''.join(numbers[6:8]),
        ''.join(numbers[8:10]),
        ''.join(numbers[10:]),
    )


def get_generate_link_whatsapp(phone, message):
    url = 'https://api.whatsapp.com/send/'
    parameter_end = "&type=phone_number&app_absent=0"
    # URL-кодирование строки
    encoded_string = quote(message, safe='')
    return url + f"?phone={phone}&text={encoded_string}" + parameter_end