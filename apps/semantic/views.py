from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.semantic.models import KipoOntology


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def query_sparql(request):
    if request.method == 'POST':
        if request.data["query"]:
            ret = KipoOntology.querySPARQL(request.data["query"])
            return Response(ret, status=201)
        else:
            return Response(request.data, status=404)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_owl_classes(request):
    onto = KipoOntology.getOntology()
    cls_owl = list(onto.classes())
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
    onto = KipoOntology.getOntology()
    ind_owl = list(onto.individuals())
    listRetorno = []
    for i in ind_owl:
        listRetorno.append(
            {
                'storid': i.storid,
                'name': i.name
            }
        )
    return Response(listRetorno)
