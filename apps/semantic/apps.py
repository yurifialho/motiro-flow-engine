from django.apps import AppConfig
from django.conf import settings
from apps.semantic.kipo_ontology import KipoOntology


class SemanticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.semantic'
    kipo_ontology = None

    def ready(self) -> None:
        import apps.semantic.signals
        self.kipo_ontology = KipoOntology(config=settings.SEMANTIC).prepareDatabase()#KipoOntology(config = SEMANTIC).prepareDatabase()
        return super().ready()

