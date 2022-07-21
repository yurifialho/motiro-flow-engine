import logging
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.kipco.models import ProcessGoal
from apps.kipco.models import ActivityGoal
from apps.kipco.models import IntensiveProcess
from apps.kipco.models import AgentType
from apps.kipco.models import AgentSpecialty
from apps.kipco.models import Activity
from apps.kipco.models import Socialization
from apps.kipco.models import Intention
from apps.kipco.models import Agent
from apps.kipco.models import Desire
from apps.kipco.models import Document
from apps.kipco.models import Placeholder
from apps.kipco.models import DataObject
from apps.kipco.serializers import ProcessGoalSerializer
from apps.kipco.serializers import ActivityGoalSerializer
from apps.kipco.serializers import IntensiveProcessSerializer
from apps.kipco.serializers import AgentTypeSerializer
from apps.kipco.serializers import AgentSpecialtySerializer
from apps.kipco.serializers import ActivitySerializer
from apps.kipco.serializers import IntentionSerializer
from apps.kipco.serializers import AgentSerializer
from apps.kipco.serializers import DesireSerializer
from apps.kipco.serializers import SocializationSerializer
from apps.kipco.serializers import DataObjectSerializer
from django.apps import apps

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def intensive_process_list(request):
    if request.method == 'GET':
        items = IntensiveProcess.objects.order_by("name")
        serializer = IntensiveProcessSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = IntensiveProcessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def intensive_process_detail(request, pk):
    try:
        item = IntensiveProcess.objects.get(pk=pk)
    except IntensiveProcess.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = IntensiveProcessSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IntensiveProcessSerializer(item, data=request.data)
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
def processgoal_list(request):
    if request.method == 'GET':
        items = ProcessGoal.objects.order_by('pk')
        serializer = ProcessGoalSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProcessGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def processgoalowl_list(request):
    if request.method == 'GET':
        items = ProcessGoal.Owl().list()
        serializer = ProcessGoalSerializer(items, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def processgoal_detail(request, pk):
    try:
        item = ProcessGoal.objects.get(pk=pk)
    except ProcessGoal.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ProcessGoalSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProcessGoalSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def activity_list(request):
    if request.method == 'GET':
        items = Activity.objects.order_by('pk')
        serializer = ActivitySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def activity_by_process_list(request, pk):
    items = Activity.objects.filter(container=pk)
    serializer = ActivitySerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def activityowl_list(request):
    if request.method == 'GET':
        items = Activity.Owl().list()
        serializer = ActivitySerializer(items, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, pk):
    try:
        item = Activity.objects.get(pk=pk)
    except Activity.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ActivitySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivitySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def activitygoal_list(request):
    if request.method == 'GET':
        items = ActivityGoal.objects.order_by('pk')
        serializer = ActivityGoalSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ActivityGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def activitygoalowl_list(request):
    if request.method == 'GET':
        items = ActivityGoal.Owl().list()
        serializer = ActivityGoalSerializer(items, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def activitygoal_detail(request, pk):
    try:
        item = ActivityGoal.objects.get(pk=pk)
    except ActivityGoal.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ActivityGoalSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivityGoalSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def intention_list(request):
    if request.method == 'GET':
        items = Intention.objects.order_by('pk')
        serializer = IntentionSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IntentionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def intention_detail(request, pk):
    try:
        item = Intention.objects.get(pk=pk)
    except Intention.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = IntentionSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IntentionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def desire_list(request):
    if request.method == 'GET':
        items = Desire.objects.order_by('pk')
        serializer = DesireSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DesireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def desire_detail(request, pk):
    try:
        item = Desire.objects.get(pk=pk)
    except Desire.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = DesireSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DesireSerializer(item, data=request.data)
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
def agenttype_list(request):
    if request.method == 'GET':
        items = AgentType.objects.order_by('pk')
        serializer = AgentTypeSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AgentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agenttype_detail(request, pk):
    try:
        item = AgentType.objects.get(pk=pk)
    except AgentType.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AgentTypeSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AgentTypeSerializer(item, data=request.data)
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
def agentspecialty_list(request):
    if request.method == 'GET':
        items = AgentSpecialty.objects.order_by('pk')
        serializer = AgentSpecialtySerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AgentSpecialtySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agentspecialty_detail(request, pk):
    try:
        item = AgentSpecialty.objects.get(pk=pk)
    except AgentSpecialty.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AgentSpecialtySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AgentSpecialtySerializer(item, data=request.data)
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
def agent_list(request):
    if request.method == 'GET':
        items = Agent.objects.order_by('pk')
        serializer = AgentSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agent_detail(request, pk):
    try:
        item = Agent.objects.get(pk=pk)
    except Agent.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AgentSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AgentSerializer(item, data=request.data)
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
def socialization_list(request):
    if request.method == 'GET':
        items = Socialization.objects.order_by('pk')
        serializer = SocializationSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SocializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def socialization_detail(request, pk):
    try:
        item = Socialization.objects.get(pk=pk)
    except Socialization.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SocializationSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SocializationSerializer(item, data=request.data)
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
def document_list(request):
    if request.method == 'GET':
        ret_docs = Document.find_all_with_badges()
        return Response(ret_docs)

    elif request.method == 'POST':
        doc = Document()
        doc.setProperties("l_name", request.data['name'])
        doc.setProperties("l_tipo", request.data['tipo'])
        doc.save()
        doc.add_equals_to(Placeholder)

        return Response(doc.to_map())

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def document_detail(request, pk):

    item = Document.find_by_id(pk)

    if item is None:
        return Response(status=404)

    if request.method == 'GET':
        return Response(item.to_map())

    elif request.method == 'PUT':
        return Response({}, status=504)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def data_object_list(request):
    if request.method == 'GET':
        items = DataObject.objects.order_by('pk')
        serializer = DataObjectSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DataObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def data_object_detail(request, pk):
    try:
        item = DataObject.objects.get(pk=pk)
    except DataObject.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = DataObjectSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DataObjectSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)
