from __future__ import annotations
import logging
import hashlib
from datetime import date, datetime
from django.db import models
from django.conf import settings
from django.apps import apps
from apps.semantic.kipo_ontology import KipoOntology
from apps.semantic.kipo_ontology import transaction
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
    #initialProperties = None

    class Meta:
        abstract = True

    def __init__(self) -> None:
        self.owl = None
        self.id = None
        self.storid = None
        self.properties = []
        #self.initialProperties = []


    @transaction
    def save(self, sync: bool = False) -> int:

        conn = KipoOntology.getConnection()
        kipo = conn.getOntology()

        with kipo:
            if self.id is None:
                self.id = self.generateHashId()
                owl = kipo[self.semanticClass](self.id)
            else:
                owl = kipo[self.id]
            self.storid = owl.storid
            self.owl = owl

            for prop in self.properties:
                conn.generateDataProperty(prop['name'],
                                            prop['value'])
                owlPropValue = getattr(owl, prop['name'])
                if owlPropValue is not None and len(owlPropValue) > 0:
                    owlPropValue.clear()
                owlPropValue.append(prop['value'])

        conn.save()

        if sync:
            conn.sync()

        return self.storid


    def setProperties(self, name: str, value) -> None:
        if type(value) == list:
            return
        found = False
        for prop in self.properties:
            if prop["name"] == name:
                prop["value"] = value
        if not found:
            self.properties.append({"name": name, "value": value})

    def unsetProperties(self, name: str) -> None:
        self.setProperties(name, None)

    @transaction
    def delete(self, sync: bool = False):
        conn = KipoOntology.getConnection()
        kipo = conn.getOntology()
        conn.delete(kipo[self.id], sync=sync)
        conn.save()

        self.owl = None
        self.storid = None
        self.id = None

    @transaction
    def to_map(self) -> map:
        mObj = {}
        if self.id is not None:
            mObj = {'storid': self.storid, 'id': self.id}
        
            conn = KipoOntology.getConnection()
            kipo = conn.getOntology()
            with kipo:
                props = kipo[self.id].get_properties()
                for prop in props:
                    if type(prop) == DataPropertyClass:
                        propValue = getattr(kipo[self.id], prop.name)
                        if propValue:
                            mObj[prop.name] = propValue[0]
                        else:
                            mObj[prop.name] = ""

        for defProps in self.initialProperties:
            if defProps not in mObj:
                mObj[defProps] = ""

        return mObj

    @transaction
    def add_equals_to(self, toClass) -> bool:
        conn = KipoOntology.getConnection()
        ret = conn.addEqualsTo(self.semanticClass,
                               toClass.semanticClass,
                               self.storid)
        conn.close()
        return ret

    @classmethod
    def generateHashId(cls) -> str:
        strId = cls.semanticClass+"__"+str(datetime.now())
        hashObj = hashlib.sha1(strId.encode())
        return hashObj.hexdigest()

    @classmethod
    def getInitialProperties(cls) -> list:
        logger.info(cls)
        return cls.initialProperties

    @classmethod
    def getInstance(cls, owl: ThingClass) -> NewSemanticModel:
        if not owl:
            raise ValueError("Owl object is required")

        obj = cls()
        obj.owl = owl
        obj.id = owl.name
        obj.storid = owl.storid
        return obj

    @classmethod
    @transaction
    def find_by_storid(cls, storid: int):
        conn = KipoOntology.getConnection()
        kipo = conn.getOntology()
        with kipo:
            owls = kipo[cls.semanticClass].instaces()
            for owl in owls:
                if owl.storid == storid:
                    return cls.getInstance(owl)

        return None

    @classmethod
    @transaction
    def find_by_id(cls, id: str) -> NewSemanticModel:
        conn = KipoOntology.getConnection()
        kipo = conn.getOntology()
        with kipo:
            owl = kipo[id]
            if owl is not None:
                return cls.getInstance(owl)

        return None

    @classmethod
    @transaction
    def find_all(cls) -> list:
        conn = KipoOntology.getConnection()
        kipo = conn.getOntology()
        all = []
        with kipo:
            for owl in kipo[cls.semanticClass].instances():
                obj = cls.getInstance(owl)
                all.append(obj.to_map())
        return all

    @classmethod
    @transaction
    def find_all_with_badges(cls) -> list:
        conn = KipoOntology.getConnection()
        kipo = conn.getOntology()
        all = []
        with kipo:
            for owl in kipo[cls.semanticClass].instances():
                obj = cls.getInstance(owl)
                objMap = obj.to_map()
                objMap['badge'] = []
                for badge in obj.owl.is_a:
                    logger.debug(f"Badge for {obj.id} is {badge.name}")
                    if badge.name not in objMap['badge']:
                        objMap['badge'].append(badge.name)
                all.append(objMap)

        return all
