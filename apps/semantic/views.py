from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.apps import apps


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def query_sparql(request):
    if request.method == 'POST':
        if request.data["query"]:
            onto = apps.get_app_config('semantic').kipo_ontology
            ret = onto.querySPARQL(request.data["query"])
            return Response(ret, status=201)
        else:
            return Response(request.data, status=404)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_owl_classes(request):
    onto = apps.get_app_config('semantic').kipo_ontology
    kipo = onto.getOntology()
    cls_owl = list(kipo.classes())
    listRetorno = []
    for i in cls_owl:
        listRetorno.append(
            {
                'storid': i.storid,
                'name': i.name
            }
        )
    return Response(listRetorno)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_owl_instances(request):
    onto = apps.get_app_config('semantic').kipo_ontology
    kipo = onto.getOntology()
    ind_owl = list(kipo.individuals())
    listRetorno = []
    for i in ind_owl:
        listRetorno.append(
            {
                'storid': i.storid,
                'name': i.name
            }
        )
    return Response(listRetorno)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sync(request):
    onto = apps.get_app_config('semantic').kipo_ontology
    onto.sync()
