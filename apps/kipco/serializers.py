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
from apps.kipco.models import Socialization
from apps.kipco.models import DataObject


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

    class Meta:
        model = Agent
        fields = '__all__'


class SocializationSerializer(ModelSerializer):

    class Meta:
        model = Socialization
        fields = '__all__'

class DataObjectSerializer(ModelSerializer):

    class Meta:
        model = DataObject
        fields = ('name', 'description', 'data', 'badges', 'storid')
