from __future__ import annotations
import logging
import hashlib
from datetime import date, datetime
from typing import Any
from django.db import models
from django.conf import settings
from django.apps import apps
from apps.semantic.kipo_ontology import KipoOntology
from apps.semantic.kipo_ontology import transaction
from owlready2 import ThingClass
from owlready2.prop import DataPropertyClass
from owlready2.prop import ObjectPropertyClass

# ---
logger = logging.getLogger(__name__)


class NewSemanticModel:

    semanticClass = None
    initialProperties = None

    class Meta:
        abstract = True

    def __init__(self) -> None:
        self.owl = None
        self.id = None
        self.storid = None
        self.properties = []
        self.complexProperties = []

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
                self.setOwlAttribute(owl, prop['name'], prop['value'])
            
            self.processComplexProperties(owl)

        conn.save()

        if sync:
            conn.sync()

        return self.storid


    def setProperties(self, name: str, value: Any) -> None:
        if type(value) == list and value is not None:
            self.setComplexProperties(self.complexProperties,name, value)
        else:
            self.setComplexProperties(self.properties, name, value)

    def unsetProperties(self, name: str) -> None:
        for prop in self.complexProperties:
            if prop['name'] == name:
                self.setProperties(name, [])
                return 
        self.setProperties(name, None)

    def setComplexProperties(self, properties: list, name: str, value: list) -> None:
        found = False
        for prop in properties:
            if prop['name'] == name:
                prop['name'] = value
        if not found:
            properties.append({"name": name, "value": value})

    def processComplexProperties(self, owl: ThingClass) -> None:
        pass
    
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
                    propValue = getattr(kipo[self.id], prop.name)
                    if type(prop) == DataPropertyClass:
                        if propValue:
                            mObj[prop.name] = propValue[0]
                        else:
                            mObj[prop.name] = ""
                    elif type(prop) == ObjectPropertyClass:
                        self.to_map_complex(mObj, prop.name, propValue)

        for defProps in self.initialProperties:
            if defProps not in mObj:
                mObj[defProps] = ""

        return mObj

    @transaction
    def to_map_complex(self, map: map, prop: str, owl: ThingClass) -> map:
        pass

    @transaction
    def add_equals_to(self, toClass) -> bool:
        conn = KipoOntology.getConnection()
        ret = conn.addEqualsTo(self.semanticClass,
                               toClass.semanticClass,
                               self.storid)
        conn.close()
        return ret

    @classmethod
    def setOwlAttribute(cls, owl: ThingClass, name: str, value: Any) -> None:
        owlPropValue = getattr(owl, name)
        if owlPropValue is not None and len(owlPropValue) > 0:
            owlPropValue.clear()
        if type(value) == list:
            for val in value:
                owlPropValue.append(val)
        else:
            owlPropValue.append(value)

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
