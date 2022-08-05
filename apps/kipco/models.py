from __future__ import annotations
import logging
from apps.semantic.models import NewSemanticModel
from apps.semantic.kipo_ontology import KipoOntology
from owlready2 import ThingClass

logger = logging.getLogger(__name__)

class ProcessGoal(NewSemanticModel):
    semanticClass = 'KIPCO__Process_Goal'
    initialProperties = ['l_name', 'l_description']


class IntensiveProcess(NewSemanticModel):
    semanticClass = 'KIPCO__Knowledge_Intensive_Process'
    initialProperties = ['l_name', 'l_description']
    #goal = models.ForeignKey(ProcessGoal,
    #                         on_delete=models.SET_NULL,
    #                         blank=True,
    #                         null=True)


class ActivityGoal(NewSemanticModel):
    semanticClass = 'KIPCO__Activity_Goal'
    initialProperties = ['l_name', 'l_description']


class AgentType(NewSemanticModel):
    semanticClass = 'KIPCO__Knowledge_Intensive_Process'
    initialProperties = ['l_name', 'l_description']


class AgentSpecialty(NewSemanticModel):
    semanticClass = 'KIPCO__Specialty'
    initialProperties = ['l_name', 'l_description']


class DataObject(NewSemanticModel):
    semanticClass = "BPO__Data_Object"
    initialProperties = ['l_name', 'l_description']

    def processComplexProperties(self, owl: ThingClass) -> None:
        if self.complexProperties is not None and len(self.complexProperties) > 0:
            composed_by = []
            consists_of = []
            for prop in self.complexProperties:
                conn = KipoOntology.getConnection()
                kipo = conn.getOntology()
                if prop['name'] == 'data_objects':
                    for dto in prop['value']:
                        composed_by.append(kipo[dto])
                if prop['name'] == 'attributes':
                    for att in prop['value']:
                        consists_of.append(kipo[att])
            if len(composed_by) > 0:
                self.setOwlAttribute(owl, 'composed_by', composed_by)
            if len(consists_of) > 0:
                self.setOwlAttribute(owl, 'consists_of', consists_of)

    def to_map_complex(self, map: map,  prop: str, owl: ThingClass, isComplement: bool = False) -> map:
        if "attributes" not in map:
            map["attributes"] = set()
        
        if not isComplement:
            map["attributes"].update(self.prepare_list_complex('consists_of', prop, owl,  Attribute.semanticClass))
        
        if "data_objects" not in map:
            map["data_objects"] = set()
        
        if not isComplement:
            map["data_objects"].update(self.prepare_list_complex('composed_by', prop, owl,  DataObject.semanticClass))

        return map


class Message(NewSemanticModel):
    semanticClass = "CO__COM__Message"
    initialProperties = ['l_title']
    #objects = models.ManyToManyField(DataObject,
    #                                 blank=True)


class Intention(NewSemanticModel):
    semanticClass = 'Intention'
    initialProperties = ['l_name', 'l_description']
    #goals = models.ManyToManyField(ActivityGoal,
    #                               blank=True)


class Desire(Intention):
    semanticClass = 'KIPCO__Desire'


class Agent(NewSemanticModel):
    semanticClass = 'KIPCO__Agent'
    initialProperties = ['l_name']
    #specialties = models.ManyToManyField(AgentSpecialty, blank=True)
    #desires = models.ManyToManyField(Desire, blank=True)
    #type = models.ForeignKey(AgentType,
    #                         on_delete=models.CASCADE,
    #                         blank=True,
    #                         null=True)


class Socialization(NewSemanticModel):
    semanticClass = "KIPCO__Socialization"
    initialProperties = ['l_name', 'l_description']
    #communications = models.ManyToManyField(Message,
    #                                        blank=True)
    #participants = models.ManyToManyField(Agent,
    #                                      blank=True)


class Activity(NewSemanticModel):
    initialProperties = ['l_name', 'l_description']
    semanticClass = 'KIPCO__Knowledge_Intensive_Activity'
    #agent = models.ForeignKey(Agent,
    #                          on_delete=models.SET_NULL,
    #                          blank=True,
    #                          null=True)
    #goal = models.ForeignKey(ActivityGoal,
    #                         on_delete=models.SET_NULL,
    #                         blank=True,
    #                         null=True)


class Association(NewSemanticModel):
    semanticClass = "BPO__Association"
    #activity = models.ForeignKey(Activity,
    #                             on_delete=models.CASCADE)
    #data_objects = models.ForeignKey(DataObject,
    #                                 on_delete=models.CASCADE)


class MessageFlow(NewSemanticModel):
    semanticClass = "BPO__Message_Flow"
    '''
    association = models.OneToOneField(Association,
                                       on_delete=models.CASCADE)
    source = models.ForeignKey(Activity,
                               related_name='msg_outgoing',
                               on_delete=models.CASCADE)
    target = models.ForeignKey(Activity,
                               related_name='msg_incoming',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    messages = models.ManyToManyField(Message,
                                      blank=True)
    socializations = models.ManyToManyField(Socialization,
                                            blank=True)
    '''

class Document(NewSemanticModel):
 
    semanticClass = "ODD__Document"
    initialProperties = ['l_name','l_description', 'l_type']

    def processComplexProperties(self, owl: ThingClass) -> None:
        logger.info(self.complexProperties)
        if self.complexProperties is not None and len(self.complexProperties) > 0:
            provides = []
            for prop in self.complexProperties:
                conn = KipoOntology.getConnection()
                kipo = conn.getOntology()
                if prop['name'] == 'data_objects':
                    for dto in prop['value']:
                        provides.append(kipo[dto])
                if prop['name'] == 'attributes':
                    for att in prop['value']:
                        provides.append(kipo[att])
            if len(provides) > 0:
                logger.info(provides)
                self.setOwlAttribute(owl, 'provides', provides)

    def to_map_complex(self, map: map,  prop: str, owl: ThingClass, isComplement: bool = False) -> map:
        if "attributes" not in map:
            map["attributes"] = set()
        
        if not isComplement:
            map["attributes"].update(self.prepare_list_complex('provides', prop, owl,  Attribute.semanticClass))
        
        if "data_objects" not in map:
            map["data_objects"] = set()
        
        if not isComplement:
            map["data_objects"].update(self.prepare_list_complex('provides', prop, owl,  DataObject.semanticClass))

        return map


class Placeholder(NewSemanticModel):
    semanticClass = "ODD__Placeholder"

class Attribute(NewSemanticModel):
    semanticClass = "ODD__Attribute"
    initialProperties = ['l_name', 'l_value']
