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
from apps.semantic.serializers import SerializerUtil
from apps.kipco.processor import RequestProcessor

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def intensive_process_list(request):
    return RequestProcessor.generic_process_list(IntensiveProcess, request)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def intensive_process_detail(request, pk):
    return RequestProcessor.generic_process_detail(IntensiveProcess, request, pk)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def processgoal_list(request):
    return RequestProcessor.generic_process_list(ProcessGoal, request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def processgoal_detail(request, pk):
    return RequestProcessor.generic_process_detail(ProcessGoal, request, pk)


@api_view(['GET', 'POST'])
def activity_list(request):
    return RequestProcessor.generic_process_list(Activity, request)


@api_view(['GET'])
def activity_by_process_list(request, pk):
    items = Activity.objects.filter(container=pk)
    serializer = ActivitySerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, pk):
    return RequestProcessor.generic_process_detail(Activity, request, pk)


@api_view(['GET', 'POST'])
def activitygoal_list(request):
    return RequestProcessor.generic_process_list(ActivityGoal, request)

@api_view(['GET', 'PUT', 'DELETE'])
def activitygoal_detail(request, pk):
    return RequestProcessor.generic_process_detail(ActivityGoal, request, pk)


@api_view(['GET', 'POST'])
def intention_list(request):
    return RequestProcessor.generic_process_list(Intention, request)


@api_view(['GET', 'PUT', 'DELETE'])
def intention_detail(request, pk):
    return RequestProcessor.generic_process_detail(Intention, request, pk)


@api_view(['GET', 'POST'])
def desire_list(request):
    return RequestProcessor.generic_process_list(Desire, request)


@api_view(['GET', 'PUT', 'DELETE'])
def desire_detail(request, pk):
    return RequestProcessor.generic_process_detail(Desire, request, pk)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agenttype_list(request):
    return RequestProcessor.generic_process_list(AgentType, request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agenttype_detail(request, pk):
    return RequestProcessor.generic_process_detail(AgentType, request, pk)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agentspecialty_list(request):
    return RequestProcessor.generic_process_list(AgentSpecialty, request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agentspecialty_detail(request, pk):
    return RequestProcessor.generic_process_detail(AgentSpecialty, request, pk)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agent_list(request):
    return RequestProcessor.generic_process_list(Agent, request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agent_detail(request, pk):
    return RequestProcessor.generic_process_detail(Agent, request, pk)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def socialization_list(request):
    return RequestProcessor.generic_process_list(Socialization, request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def socialization_detail(request, pk):
    return RequestProcessor.generic_process_detail(Socialization, request, pk)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def document_list(request):
    return RequestProcessor.generic_process_list(Document, request)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def document_detail(request, pk):
    return RequestProcessor.generic_process_detail(Document, request, pk)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def data_object_list(request):
    return RequestProcessor.generic_process_list(DataObject, request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def data_object_detail(request, pk):
    return RequestProcessor.generic_process_detail(Document, request, pk)
