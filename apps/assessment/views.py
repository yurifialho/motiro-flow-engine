from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.assessment.models import Criteria
from apps.assessment.models import Quiz
from apps.assessment.models import Answer
from apps.assessment.serializers import CriteriaSerializer
from apps.assessment.serializers import QuizSerializer
from apps.assessment.serializers import AnswerSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def criteria_list(request):
    if request.method == 'GET':
        items = Criteria.objects.order_by("level")
        serializer = CriteriaSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CriteriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def criteria_detail(request, pk):
    try:
        item = Criteria.objects.get(pk=pk)
    except Criteria.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CriteriaSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CriteriaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def quiz_list(request):
    if request.method == 'GET':
        items = Quiz.objects.order_by("level")
        serializer = QuizSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def quiz_detail(request, pk):
    try:
        item = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = QuizSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuizSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def answer_list(request):
    if request.method == 'GET':
        items = Answer.objects.order_by("level")
        serializer = AnswerSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def answer_detail(request, pk):
    try:
        item = Answer.objects.get(pk=pk)
    except Answer.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AnswerSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AnswerSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)