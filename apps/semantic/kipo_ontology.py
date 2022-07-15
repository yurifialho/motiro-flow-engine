import logging
import threading
import time
import os
import sys
from owlready2 import World
from owlready2 import ThingClass
from owlready2 import onto_path
from owlready2 import sync_reasoner_pellet
from owlready2 import destroy_entity

logger = logging.getLogger(__name__)

class KipoOntology:

    __lock = threading.Lock()

    def __init__(self, config, reload : bool = False, debug : bool = False) -> None:
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
                        sync_reasoner_pellet(x = self.__world, infer_property_values=True, debug = debug)
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
                    logger.error('Connot load owl file! [Retrying in ' + str(tries*5) + ' sec]')
                    logger.error(e)
                    time.sleep(tries*5)
        return self

    def loadConfig(self, sync : bool = True):
        try:
            logger.info("Loading ontologies....")
            self.__world = World(filename=self.__config["DATABASE"]["NAME"], exclusive=False)
            self.__kipo = self.__world.get_ontology(self.__config["OWL_FILES"]["ONTOLOGY_IRI"]).load()

            if sync:
                self.sync()
            logger.info("Ontologies loaded.")
        except Exception as e:
            logger.error(e)

    def getOntology(self):
        self.loadConfig(sync=False)
        if not self.__kipo:
            raise Exception("Ontology is not loaded!")
        return self.__kipo

    def getWorld(self):
        self.loadConfig(sync=False)
        if not self.__world:
            raise Exception("Ontology is not loaded!")
        return self.__world

    def save(self, sync : bool = False):
        world = self.getWorld()
        world.save()
        world.close()
        if sync:
            self.sync(world)
    
    def delete(self, owl : ThingClass , sync : bool = False):
        destroy_entity(self.owl)

        if sync:
            self.sync()

    def querySPARQL(self, query):
        try:
            l = self.getWorld().sparql(query)
            return list(l)
        except Exception as e:
            logger.error(e)
            return None
    
    def sync(self, world : World = None) -> None :
        logger.info("Sync world with reasoner.....")
        if not world:
            world = self.getWorld()
        if not world:
            raise Exception('World is None. You need have a initialized world')            
        debug = 2 if self.debug else 1 
        sync_reasoner_pellet(x = world, infer_property_values=True, debug = debug)
        logger.info("Sync finished.")
    

    def getBadges(self, semanticClass : str, storid : int ) -> list:
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

    def addEqualsTo(self, semanticClass : str, toClass : str, storid : int) -> bool:
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