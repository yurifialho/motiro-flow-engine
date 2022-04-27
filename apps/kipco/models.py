from django.db import models
from apps.bpmn.models import Activity as BpmnActivity, FlowElementsContainer
from apps.semantic.models import SemanticModel


class ProcessGoal(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    semanticClass = 'KIPCO__Process_Goal'

    def __str__(self):
        return self.name


class IntensiveProcess(SemanticModel, FlowElementsContainer):

    goal = models.ForeignKey(ProcessGoal,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)

    semanticClass = 'KIPCO__Knowledge_Intensive_Process'

    def setIndividualProperties(self, owl):
        if self.goal and self.goal.getIndividual():
            owl.has.append(self.goal.getIndividual())


class ActivityGoal(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    semanticClass = 'KIPCO__Activity_Goal'

    def __str__(self):
        return self.name


class AgentType(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    semanticClass = 'KIPCO__Knowledge_Intensive_Process'

    def __str__(self):
        return self.name


class AgentSpecialty(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    semanticClass = 'KIPCO__Specialty'

    def __str__(self):
        return self.name


class DataObject(SemanticModel):
    data = models.TextField(max_length=1000)

    semanticClass = "BPO__Data_Object"

    def __str__(self):
        return self.name


class Message(SemanticModel):
    data = models.TextField(max_length=1000)
    objects = models.ManyToManyField(DataObject,
                                     blank=True)

    semanticClass = "CO__COM__Message"

    def __str__(self):
        return self.name


class Intention(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    goals = models.ManyToManyField(ActivityGoal,
                                   blank=True)

    semanticClass = 'Intention'

    def __str__(self):
        return self.name


class Desire(Intention):

    semanticClass = 'KIPCO__Desire'

    def __str__(self):
        return self.name


class Agent(SemanticModel):
    name = models.CharField(max_length=100)
    specialties = models.ManyToManyField(AgentSpecialty, blank=True)
    desires = models.ManyToManyField(Desire, blank=True)
    type = models.ForeignKey(AgentType,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)

    semanticClass = 'KIPCO__Agent'

    def __str__(self):
        return self.name


class Socialization(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    communications = models.ManyToManyField(Message,
                                            blank=True)
    participants = models.ManyToManyField(Agent,
                                          blank=True)

    semanticClass = "KIPCO__Socialization"

    def __str__(self):
        return self.name


class Activity(SemanticModel, BpmnActivity):
    agent = models.ForeignKey(Agent,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    goal = models.ForeignKey(ActivityGoal,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)

    semanticClass = 'KIPCO__Knowledge_Intensive_Activity'

    def __str__(self):
        return self.name


class Association(SemanticModel):
    activity = models.ForeignKey(Activity,
                                 on_delete=models.CASCADE)
    data_objects = models.ForeignKey(DataObject,
                                     on_delete=models.CASCADE)

    semanticClass = "BPO__Association"

    def __str__(self):
        return self.name


class MessageFlow(SemanticModel):
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

    semanticClass = "BPO__Message_Flow"

    def __str__(self):
        return self.name
