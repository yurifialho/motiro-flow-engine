from rest_framework.serializers import ModelSerializer
from apps.assessment.models import Criteria
from apps.assessment.models import Quiz
from apps.assessment.models import Answer


class CriteriaSerializer(ModelSerializer):

    class Meta:
        model = Criteria
        fields = '__all__'


class QuizSerializer(ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'


class AnswerSerializer(ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
