from django.apps import AppConfig


class SemanticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.semantic'

    def ready(self) -> None:
        import apps.semantic.signals
        return super().ready()

