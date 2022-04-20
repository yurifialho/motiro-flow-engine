from rest_framework.serializers import ModelSerializer
from apps.kipco.models import IntensiveProcess
from apps.kipco.models import ProcessGoal
from apps.kipco.models import Activity
from apps.kipco.models import ActivityGoal
from apps.kipco.models import Intention
from apps.kipco.models import Desire
from apps.kipco.models import AgentType
from apps.kipco.models import AgentSpecialty
from apps.kipco.models import Agent


class IntensiveProcessSerializer(ModelSerializer):

    class Meta:
        model = IntensiveProcess
        fields = '__all__'


class ProcessGoalSerializer(ModelSerializer):

    class Meta:
        model = ProcessGoal
        fields = '__all__'


class ActivitySerializer(ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'


class ActivityGoalSerializer(ModelSerializer):

    class Meta:
        model = ActivityGoal
        fields = '__all__'


class IntentionSerializer(ModelSerializer):

    class Meta:
        model = Intention
        fields = '__all__'


class DesireSerializer(ModelSerializer):

    class Meta:
        model = Desire
        fields = '__all__'


class AgentTypeSerializer(ModelSerializer):

    class Meta:
        model = AgentType
        fields = '__all__'


class AgentSpecialtySerializer(ModelSerializer):

    class Meta:
        model = AgentSpecialty
        fields = '__all__'


class AgentSerializer(ModelSerializer):
    '''
    specialties = AgentSpecialtySerializer(many=True)
    desires = DesireSerializer(many=True)

    def create(self, validated_data):
        spec = validated_data.pop('specialties')
        specSaved = []
        for s in spec:
            if 'id' not in s:
                sv = AgentSpecialty.objects.create(**s)
            else:
                print("Getting Specialty by pk")
                sv = AgentSpecialty.objects.get(pk=s['id'])
            specSaved.append(sv)
        des = validated_data.pop('desires')
        desSaved = []
        for d in des:
            if 'id' not in d:
                dv = Desire.objects.create(**d)
            else:
                print("Getting Desire by pk")
                dv = Desire.objects.get(pk=d['id'])
            desSaved.append(dv)
        agent = Agent.objects.create(**validated_data)
        agent.specialties.set(specSaved)
        agent.desires.set(desSaved)
        return agent
    '''
    class Meta:
        model = Agent
        fields = '__all__'
