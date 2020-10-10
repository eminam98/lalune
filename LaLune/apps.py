from django.apps import AppConfig


class LaluneConfig(AppConfig):
    name = 'LaLune'

    def ready(self):
        import LaLune.signals








