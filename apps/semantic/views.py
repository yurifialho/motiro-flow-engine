import time
import logging
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.semantic.kipo_ontology import KipoOntology

logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def query_sparql(request):
    if request.method == 'POST':
        if request.data["query"]:
            conn = KipoOntology.getConnection()
            ret = conn.querySPARQL(request.data["query"])
            return Response(ret, status=201)
        else:
            return Response(request.data, status=404)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_owl_classes(request):
    conn = KipoOntology.getConnection()
    kipo = conn.getOntology()
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
    conn = KipoOntology.getConnection()
    kipo = conn.getOntology()
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
    try:
        start_time = time.time()
        conn = KipoOntology.getConnection()
        if not conn.isLoaded():
            conn.loadConfig(sync=False)
        conn.save(sync=True)
        end_time = time.time()
        return Response({'status': 'done',
                         'time': round(end_time - start_time, 2)},
                        status=200)
    except Exception as e:
        logger.error(e)
        return Response(status=500)
