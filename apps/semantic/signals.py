import logging
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
#from apps.semantic.models import SemanticModel

logger = logging.getLogger(__name__)


@receiver(pre_save)
def pre_save(sender, instance, **kwargs):
    pass
    '''
    if SemanticModel in instance.__class__.__bases__:
        if not instance.semanticClass:
            raise Exception("Semantic Class not defined")

        kipo = KipoOntology.getOntology()
        with kipo:
            try:
                ontoInd = instance.getIndividual()
                if not ontoInd:
                    ontoInd = instance.objToOwl()
                instance.storid = ontoInd.storid
            except Exception as e:
                logger.error(e)
                raise(e)
            finally:
                KipoOntology.save()
    '''


@receiver(post_save)
def post_save(sender, instance, **kwargs):
    if SemanticModel in instance.__class__.__bases__:
        pass

#@receiver(post_delete)
#def post_delete(sender, instance, **kwargs):
#    if SemanticModel in instance.__class__.__bases__:
#        if not instance.semanticClass:
#            raise Exception("Semantic Class not defined")