from distutils.debug import DEBUG
import time
import logging
import threading
from django.db import models
from django.conf import settings
from owlready2 import World, onto_path, sync_reasoner_pellet
from rdflib import plugin 
from rdflib.serializer import Serializer
# ---
logger = logging.getLogger(__name__)


class KipoOntology:
    _lock = threading.Lock()

    @classmethod
    def loadConfig(cls):
        with cls._lock:
            if not hasattr(cls, '_world') or cls._world == None:
                loaded = False
                tries = 0
                while not loaded and tries < 4:
                    try:
                        # Open 1 World - It's for test and development use
                        # TODO: Create one World for each Process Instance
                        logger.info("Loading ontologies....")
                        cls._world = World(filename=settings.SEMANTIC["DATABASE"]["NAME"], exclusive=False)
                        onto_path.append(settings.SEMANTIC["OWL_FILES"]["IMPORT_FOLDER"])
                        cls._world.get_ontology(settings.SEMANTIC["OWL_FILES"]["OWL_PATH_FILE"]).load()
                        cls._kipo = cls._world.get_ontology(settings.SEMANTIC["OWL_FILES"]["ONTOLOGY_IRI"]).load()
                        cls.sync()
                        cls._world.save()
                        loaded = cls._kipo.loaded
                        logger.info("Ontologies loaded.")
                    except Exception as e:
                        tries += 1
                        logger.info(settings.SEMANTIC["OWL_FILES"]["OWL_PATH_FILE"])
                        logger.error('Connot load owl file! [Retrying in ' + str(tries*5) + ' sec]')
                        logger.error(e)
                        time.sleep(tries*5)

    @classmethod
    def getOntology(cls):
        if not hasattr(cls, '_kipo'):
            cls.loadConfig()
        return cls._kipo

    @classmethod
    def getWorld(cls):
        if not hasattr(cls, '_world'):
            cls.loadConfig()
        return cls._world

    @classmethod
    def save(cls):
        world = cls.getWorld()
        cls.sync(world)
        world.save()

    @classmethod
    def querySPARQL(cls, query):
        try:
            l = cls.getWorld().sparql(query)
            return list(l)
        except Exception:
            return None
    
    @classmethod
    def sync(cls, world : World = None) -> None :
        logger.info("Sync world with reasoner.....")
        if not world:
            world = cls._world
        if not world:
            raise Exception('World is None. You need have a initialized world')            
        debug = 2 if settings.DEBUG else 1 
        sync_reasoner_pellet(x = world, infer_property_values=True, debug = debug)
        logger.info("Sync finished.")
    
    @classmethod
    def getBadges(cls, semanticClass : str, storid : int ) -> list:
        kipo = cls.getOntology()

        badges = []
        with kipo:
            docs = kipo[semanticClass].instances()
            for doc in docs:
                logger.debug(doc)
                logger.debug(f"Selected[{doc.storid}]-[{storid}]")
                if doc.storid == storid:
                    for badge in doc.is_a:
                        logger.debug(f"Badge for {doc.name} is {badge.name}")
                        badges.append(badge.name)
        
        return badges
    
    @classmethod
    def addEqualsTo(cls, semanticClass : str, toClass : str, storid : int) -> bool:
        kipo = cls.getOntology()
        with kipo:
            docs = kipo[semanticClass].instances()
            for doc in docs:
                logger.debug(doc)
                logger.debug(f"Selected[{doc.storid}]-[{storid}]")
                if doc.storid == storid:
                    doc.is_a.append(kipo[toClass])
                    cls.save()
                    return True
        
        return False



class SemanticModel(models.Model):

    storid = models.IntegerField(unique=False, blank=True, null=True)
    semanticClass = 'Thing'

    def listObj(self) -> list:
        lista = []
        for k in self.listOwl():
            lista.append(self.owlToObj(k))
        return lista

    def listOwl(self) -> list:
        kipo = KipoOntology.getOntology()
        lista = kipo.search(type=self.getSemanticClass())
        return lista

    def owlToObj(self, owlObj):
        pg = self.__class__()
        pg.name = owlObj.name
        return pg

    def objToOwl(self):
        kipo = KipoOntology.getOntology()
        with kipo:
            o = self.getSemanticClass()(self.name)
            self.setIndividualProperties(o)
            KipoOntology.save()
            return o

    def isExistsIndividual(self) -> bool :
        if self.getIndividual():
            return True
        else:        
            return False

    def getIndividual(self) :
        kipo = KipoOntology.getOntology()
        for o in kipo.search(type=self.getSemanticClass()):
            if o.name == self.name:
                return o
        return None

    def getSemanticClass(self) :
        kipo = KipoOntology.getOntology()
        return kipo[self.semanticClass]

    def setIndividualProperties(self, owl):
        pass

    class Meta:
        abstract = True
