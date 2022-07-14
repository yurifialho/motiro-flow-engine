import time
import logging
import threading
from django.db import models
from django.conf import settings
from django.apps import apps
from owlready2 import ThingClass

# ---
logger = logging.getLogger(__name__)

class SemanticModel(models.Model):

    storid = models.IntegerField(unique=False, blank=True, null=True)
    semanticClass = 'Thing'

    def listObj(self) -> list:
        lista = []
        for k in self.listOwl():
            lista.append(self.owlToObj(k))
        return lista

    def listOwl(self) -> list:
        onto = apps.get_app_config('semantic').kipo_ontology
        kipo = onto.getOntology()
        lista = kipo.search(type=self.getSemanticClass())
        return lista

    def owlToObj(self, owlObj):
        pg = self.__class__()
        pg.name = owlObj.name
        return pg

    def objToOwl(self):
        onto = apps.get_app_config('semantic').kipo_ontology
        kipo = onto.getOntology()
        with kipo:
            o = self.getSemanticClass()(self.name)
            self.setIndividualProperties(o)
            onto.save()
            return o

    def isExistsIndividual(self) -> bool :
        if self.getIndividual():
            return True
        else:        
            return False

    def getIndividual(self) :
        onto = apps.get_app_config('semantic').kipo_ontology
        kipo = onto.getOntology()
        for o in kipo.search(type=self.getSemanticClass()):
            if o.name == self.name:
                return o
        return None

    def getSemanticClass(self) :
        onto = apps.get_app_config('semantic').kipo_ontology
        kipo = onto.getOntology()
        return kipo[self.semanticClass]

    def setIndividualProperties(self, owl):
        pass

    class Meta:
        abstract = True

class NewSemanticModel:

    semanticClass = None

    def __init__(self, name) -> None:
        self.onto = apps.get_app_config('semantic').kipo_ontology
        self.world = self.onto.getWorld()
        self.kipo = self.onto.getOntology()
        
        self.load_or_create(name)

    def get_owl_by_name(self, name : str) -> ThingClass:
        with self.kipo:
            objs = self.kipo[self.semanticClass].instances()
            for obj in objs:
                if obj.name == name:
                    return obj
    
    def get_owl_by_storid(self, storid : int) -> ThingClass:
        with self.kipo:
            objs = self.kipo[self.semanticClass].instances()
            for obj in objs:
                if obj.storid == storid:
                    return obj

    def load_or_create(self, name : str, storid = int):
        if not name and not storid:
            raise Exception('name not found')
        
        if name:
            obj = self.get_owl_by_name(name)
        elif storid: 
            obj = self.get_owl_by_storid(storid)
        
        if not obj and name:
            with self.kipo:
                obj = self.kipo[self.semanticClass](name)

        if not obj:
            raise Exception("Object cannot be loaded or create")
        else:
            self.owl = obj
            self.storid = obj.storid
            self.name = obj.name

    def save(self, sync : bool = False) :
        self.onto.save()

        if sync:
            self.onto.sync()
    
    def delete(self, sync : bool = False):
        self.onto.delete(self.owl, sync = sync)

        self.owl = None
        self.storid = None
        self.name = None



    def get_storid(self):
        self.storid
    
    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name : str):
        self.owl.set_name(name)
        self.name = name

    def to_map(self) -> map:
        return self.owl_to_map(self.owl)

    def add_equals_to(self, toClass) -> bool:
        kipo_ontology = apps.get_app_config('semantic').kipo_ontology
        return kipo_ontology.addEqualsTo(self.semanticClass, toClass.semanticClass, self.storid)

    @classmethod
    def owl_to_map(cls, owl) -> map:
        return {'storid':owl.storid, 'name':owl.name}

    @classmethod
    def find_all(cls) -> list:
        kipo_ontology = apps.get_app_config('semantic').kipo_ontology
        kipo = kipo_ontology.getOntology()
        all = []
        with kipo:
            for obj in kipo[cls.semanticClass].instances():
                all.append(cls.owl_to_map(obj))
        return all
    
    @classmethod
    def find_by_storid(cls, storid : int):
        kipo_ontology = apps.get_app_config('semantic').kipo_ontology

    @classmethod
    def find_all_with_badges(cls) -> list:
        kipo_ontology = apps.get_app_config('semantic').kipo_ontology
        kipo = kipo_ontology.getOntology()
        all = []
        with kipo:
            for obj in kipo[cls.semanticClass].instances():
                objMap = cls.owl_to_map(obj)
                objMap['badge'] = []
                for badge in obj.is_a:
                    logger.debug(f"Badge for {obj.name} is {badge.name}")
                    objMap['badge'].append(badge.name)
                all.append(objMap)
        return all

    