"""
Названия договоров сотрудничества потерялись (пустые во всех языках).
Восстанавливаем по имени файла: при загрузке оно строилось из названия (транслит первых 30 символов).
Заполняем только пустые записи — всё, что уже введено в админке, не трогаем.
"""
from django.db import migrations

TITLES_BY_FILE = {
    'dogovor-ubs-transit': 'Договор с «UBS Transit»',
    'dogovor-avtotsentr-estokada': 'Договор с автоцентром «Эстокада»',
    'dogovor-bpatp': 'Договор с БПАТП',
    'dogovor-deu-7': 'Договор с ДЭУ-7',
    'dogovor-deu-9': 'Договор с ДЭУ-9',
    'dogovor-deu-25': 'Договор с ДЭУ-25',
    'dogovor-deu-958': 'Договор с ДЭУ-958',
    'dogovor-osoo-avtotsentr-perekre': 'Договор с ОсОО «Автоцентр Перекрёсток»',
    'dogovor-prezidentskij-garazh': 'Договор с Президентским гаражом',
    'dogovor-9-deu': 'Договор с 9-ДЭУ',
    'dogovor-zao-shoro': 'Договор с ЗАО «Шоро»',
    'dogovor-mp-bishkek-asfaltservi': 'Договор с МП «Бишкекасфальтсервис»',
    'dogovor-osoo-bedachi': 'Договор с ОсОО «Бедачи»',
    'dogovor-osoo-dt-tehnik': 'Договор с ОсОО «ДТ Техник»',
}


def forwards(apps, schema_editor):
    Cooperation = apps.get_model('core', 'Cooperation')
    for item in Cooperation.objects.all():
        if item.title or item.title_ru:
            continue
        stem = item.file.name.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        title = TITLES_BY_FILE.get(stem)
        if title:
            Cooperation.objects.filter(pk=item.pk).update(title=title, title_ru=title)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_clean_rich_text'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
