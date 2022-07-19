from __future__ import annotations
import logging
import hashlib
from datetime import date, datetime
from django.db import models
from django.conf import settings
from django.apps import apps
from apps.semantic.kipo_ontology import KipoOntology
from owlready2 import ThingClass
from owlready2.prop import DataPropertyClass

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

    def __init__(self) -> None:
        self.owl = None
        self.id = None
        self.storid = None
        self.properties = []

    def save(self, sync : bool = False) :
        try:
            if not self.id :
                self.id = self.generateHashId()

                conn = KipoOntology.getConnection()
                kipo = conn.getOntology()
                
                with kipo:
                    owl = kipo[self.semanticClass](self.id)
                    self.storid = owl.storid
                    self.owl = owl

                    for prop in self.properties:
                        p = conn.generateDataProperty(prop['name'], prop['value'])
                        getattr(owl, prop['name']).append(prop['value'])
                        logger.info(dir(owl))
            
                conn.save()

                if sync:
                    conn.sync()

                return self
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            if conn:
                conn.close()

    def setProperties(self, name : str, value) -> None:
        found = False
        for prop in self.properties:
            if prop["name"] == name:
                prop["value"] = value
        if not found:
            self.properties.append({"name": name, "value": value })
    
    def unsetProperties(self, name : str) -> None:
        self.setProperties(name, None)

    
    def delete(self, sync : bool = False):
        self.onto.delete(self.owl, sync = sync)

        self.owl = None
        self.storid = None
        self.id = None

    def to_map(self) -> map:
        mObj = {'storid': self.storid, 'id': self.id}
        if self.owl:
            for prop in self.owl.get_properties():
                if type(prop) == DataPropertyClass:
                    propValue = getattr(self.owl, prop.name)
                    if propValue:
                        mObj[prop.name] = propValue[0]
                    else:
                        mObj[prop.name] = ""


        return mObj

    
    def add_equals_to(self, toClass) -> bool:
        try:
            conn = KipoOntology.getConnection()
            ret = conn.addEqualsTo(self.semanticClass, toClass.semanticClass, self.storid)
            conn.close()
            return ret
        except Exception as e:
            logger.error(e)
            raise(e)
        finally:
            conn.close()
    
    
    @classmethod
    def generateHashId(cls) -> str:
        strId = cls.semanticClass+"__"+str(datetime.now())
        hashObj = hashlib.sha1(strId.encode())
        return hashObj.hexdigest()

    @classmethod
    def getInstance(cls, owl : ThingClass) -> NewSemanticModel:
        if not owl:
            raise ValueError("Owl object is required")

        obj = NewSemanticModel()
        obj.owl = owl
        obj.id = owl.name
        obj.storid = owl.storid
        return obj

    @classmethod
    def find_by_storid(cls, storid : int):
        try:
            conn = KipoOntology.getConnection()
            kipo = conn.getOntology()
            with kipo:
                owls = kipo[cls.semanticClass].instaces()
                for owl in owls:
                    if owl.storid == storid:
                        return cls.getInstance(owl)
            
            return None

        except Exception as e:
            logger.error(e)
            raise e
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id : str) -> NewSemanticModel:
        try:
            conn = KipoOntology.getConnection()
            kipo = conn.getOntology()
            with kipo:
                owls = kipo[cls.semanticClass].instances()
                for owl in owls:
                    if owl.name == id:
                        return cls.getInstance(owl)
            
            return None

        except Exception as e:
            logger.error(e)
            raise e
        finally:
            conn.close()

    @classmethod
    def find_all(cls) -> list:
        try:
            conn = KipoOntology.getConnection()
            kipo = conn.getOntology()
            all = []
            with kipo:
                for owl in kipo[cls.semanticClass].instances():
                    obj = NewSemanticModel.getInstance(owl)
                    all.append(obj.to_map())
            return all
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            conn.close()

    @classmethod
    def find_all_with_badges(cls) -> list:
        try:
            conn = KipoOntology.getConnection()
            kipo = conn.getOntology()
            all = []
            with kipo:
                for owl in kipo[cls.semanticClass].instances():
                    obj = NewSemanticModel.getInstance(owl)
                    objMap = obj.to_map()
                    objMap['badge'] = []
                    for badge in obj.owl.is_a:
                        logger.debug(f"Badge for {obj.id} is {badge.name}")
                        if not badge.name in objMap['badge']:
                            objMap['badge'].append(badge.name)
                    all.append(objMap)
            
            return all
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            conn.close()
            