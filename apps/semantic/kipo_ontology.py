from __future__ import annotations
import logging
import threading
import time
import os
from django.apps import apps
from owlready2 import World
from owlready2 import ThingClass
from owlready2 import onto_path
from owlready2 import sync_reasoner_pellet
from owlready2 import destroy_entity
from owlready2 import DataProperty

logger = logging.getLogger(__name__)


def transaction(func):
    def run(*args, **kargs):
        try:
            logger.debug(f"Opening connection {str(func)}")
            conn = KipoOntology.getConnection()
            loaded = conn.isLoaded()
            if not loaded:
                logger.debug("Ontology is not loaded, loading...")
                conn.loadConfig(sync=False)
            return func(*args, **kargs)
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            if not loaded:
                logger.debug(f"Closing connection {str(func)}")
                conn.close()

    return run


class KipoOntology:

    __lock = threading.Lock()

    def __init__(self, config, reload: bool = False, debug: bool = False) -> None:
        logger.info("Starting config....")
        self.__config  = config
        self.debug = debug
        self.reload = reload
        self.__kipo = None
        self.__world = None

    def prepareDatabase(self):
        with self.__lock:
            loaded = False
            tries = 0
            while not loaded and tries < 4:
                try:
                    logger.info("Loading ontologies....")
                    if not os.path.exists(self.__config["DATABASE"]["NAME"]):
                        logger.info('Database not exists!')
                        self.__world = World(filename=self.__config["DATABASE"]["NAME"], exclusive=False)
                        onto_path.append(self.__config["OWL_FILES"]["IMPORT_FOLDER"])
                        self.__world.get_ontology(self.__config["OWL_FILES"]["OWL_PATH_FILE"]).load()
                        self.__kipo = self.__world.get_ontology(self.__config["OWL_FILES"]["ONTOLOGY_IRI"]).load()
                        debug = 2 if self.debug else 1
                        sync_reasoner_pellet(x=self.__world,
                                             infer_property_values=True,
                                             debug=debug)
                        self.__world.save()
                        loaded = self.__kipo.loaded
                        logger.info("Ontologies loaded.")
                        self.__world.close()
                    else:
                        loaded = True
                    logger.info("Semantic Database prepared.")
                except Exception as e:
                    tries += 1
                    logger.info(self.__config["OWL_FILES"]["OWL_PATH_FILE"])
                    logger.error(f'Connot load owl file! [Retrying in {str(tries*5)} sec]')
                    logger.error(e)
                    time.sleep(tries*5)
        return self

    def loadConfig(self, sync: bool = True):
        try:
            logger.debug("Loading ontologies....")
            self.__world = World(filename=self.__config["DATABASE"]["NAME"],
                                 exclusive=False)
            self.__kipo = self.__world.get_ontology(self.__config["OWL_FILES"]["ONTOLOGY_IRI"]).load()

            if sync:
                self.sync()
            logger.debug("Ontologies loaded.")
        except Exception as e:
            logger.error(e)

    def getOntology(self):
        if self.__kipo is None:
            self.loadConfig(sync=False)
        if self.__kipo is None:
            raise Exception("Ontology is not loaded!")
        return self.__kipo

    def getWorld(self):
        if self.__world is None:
            self.loadConfig(sync=False)
        if self.__world is None:
            raise Exception("Ontology is not loaded!")
        return self.__world

    def close(self, world: World = None) -> bool:
        try:
            if world is None:
                world = self.getWorld()

            world.close()
            self.__kipo = None
            self.__world = None
            return True
        except Exception as e:
            logger.error(e)
            return False

    def save(self, world: World = None, sync: bool = False):
        if world is None:
            world = self.getWorld()
        world.save()
        if sync:
            self.sync(world)

    def delete(self, owl: ThingClass, sync: bool = False) -> None:
        destroy_entity(owl)

        if sync:
            self.sync()

    def querySPARQL(self, query) -> list:
        try:
            returnedQuery = self.getWorld().sparql(query)
            return list(returnedQuery)
        except Exception as e:
            logger.error(e)
            return None

    def sync(self, world: World = None) -> None:
        logger.info("Sync world with reasoner.....")
        if world is None:
            world = self.getWorld()
        if world is None:
            raise Exception('World is None. You need have a initialized world')
        debug = 2 if self.debug else 1
        sync_reasoner_pellet(x=world,
                             infer_property_values=True,
                             debug=debug)
        logger.info("Sync finished.")

    def getBadges(self, semanticClass: str, storid: int) -> list:
        kipo = self.getOntology()

        badges = []
        with kipo:
            objs = kipo[semanticClass].instances()
            for obj in objs:
                logger.debug(obj)
                logger.debug(f"Selected[{obj.storid}]-[{storid}]")
                if obj.storid == storid:
                    for badge in obj.is_a:
                        logger.debug(f"Badge for {obj.name} is {badge.name}")
                        badges.append(badge)

        return badges

    def addEqualsTo(self,
                    semanticClass: str,
                    toClass: str,
                    storid: int) -> bool:

        kipo = self.getOntology()
        with kipo:
            objs = kipo[semanticClass].instances()
            for obj in objs:
                logger.debug(obj)
                logger.debug(f"Selected[{obj.storid}]-[{storid}]")
                if obj.storid == storid:
                    obj.is_a.append(kipo[toClass])
                    self.save()
                    return True

        return False

    def generateDataProperty(self, name: str, value) -> DataProperty:
        propertyClass = type(name,
                             (DataProperty,),
                             {"range": [str]})
        return propertyClass

    def isLoaded(self) -> bool:
        return self.__kipo is not None and self.__kipo.loaded

    @classmethod
    def getConnection(cls) -> KipoOntology:
        return apps.get_app_config('semantic').kipo_ontology
