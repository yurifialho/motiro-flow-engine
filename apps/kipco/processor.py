from __future__ import annotations
import logging
from apps.semantic.serializers import SerializerUtil
from apps.semantic.models import NewSemanticModel
from rest_framework.response import Response


class RequestProcessor():

    @classmethod
    def generic_process_list(cls, targetClass: NewSemanticModel, request) -> Response:
        if request.method == 'GET':
            items =  targetClass.find_all()
            return Response(items)

        elif request.method == 'POST':
            item = targetClass()
            SerializerUtil.populateFromRequest(item, request.data)
            item.save()
            return Response(item.to_map(), status=201)
    
    @classmethod
    def generic_process_detail(cls, targetClass: NewSemanticModel, request, pk) -> Response:
        item = targetClass.find_by_id(pk)

        if item is None:
            return Response(status=404)

        if request.method == 'GET':
            return Response(item.to_map())

        elif request.method == 'PUT':
            SerializerUtil.populateFromRequest(item, request.data)
            item.save()
            return Response(item.to_map())

        elif request.method == 'DELETE':
            item.delete()
            return Response(status=204)