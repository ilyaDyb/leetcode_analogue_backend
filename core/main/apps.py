from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.main'
    def ready(self) -> None:
        import core.main.signals
