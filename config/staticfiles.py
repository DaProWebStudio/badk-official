from django.contrib.staticfiles.apps import StaticFilesConfig


class StaticConfig(StaticFilesConfig):
    # static/ — это и исходники фронтенда: не отдаём их через collectstatic
    ignore_patterns = StaticFilesConfig.ignore_patterns + [
        'node_modules', 'src', 'scripts', 'package.json', 'package-lock.json', 'icons.txt',
    ]
