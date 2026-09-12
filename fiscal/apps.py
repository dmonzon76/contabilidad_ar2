

from django.apps import AppConfig

class FiscalConfig(AppConfig):
    name = 'fiscal'

    def ready(self):
        import fiscal.signals
