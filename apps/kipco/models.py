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
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)

    semanticClass = 'KIPCO__Knowledge_Intensive_Process'

    def setIndividualProperties(self, owl):
        if self.goal and self.goal.getIndividual():
            owl.has.append(self.goal.getIndividual())


class Activity(SemanticModel, BpmnActivity):

    semanticClass = 'KIPCO__Knowledge_Intensive_Activity'


class ActivityGoal(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    semanticClass = 'KIPCO__Activity_Goal'

    def __str__(self):
        return self.name


class Intention(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    semanticClass = 'Intention'

    def __str__(self):
        return self.name


class Desire(SemanticModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    intention = models.ForeignKey(Intention,
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)

    semanticClass = 'KIPCO__Desire'

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


class Agent(SemanticModel):
    name = models.CharField(max_length=100)
    specialties = models.ManyToManyField(AgentSpecialty)
    desires = models.ManyToManyField(Desire)
    type = models.ForeignKey(AgentType,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)

    semanticClass = 'KIPCO__Agent'

    def __str__(self):
        return self.name
