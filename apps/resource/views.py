import re
import json
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from apps.resource.models import ResourceGroup, ResourcePermission
from apps.resource.serializers import (
    ResourceGroupSerializer,
    ResourcePermissionSerializer,
)
from apps.common.permission import IsSuperUser
from apps.resource.utils import get_action

from apps.common.timescale.execute import execute_query
from apps.common.timescale.queries import QUERIES
from rest_framework.views import APIView
from apps.resource.serializers import UploadedFileSerializer
from rest_framework.parsers import MultiPartParser


class ResourceViewSet(ModelViewSet):
    serializer_class = ResourceGroupSerializer
    permission_classes = (IsAuthenticated,)

    # TODO: Optimize the query to get the resources using parent-child relationship
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ResourceGroup.objects.all()
        permissions = user.get_resource_permissions()

        action = get_action(self.action)
        resource_list = []
        for perm in permissions:
            permission = ResourcePermission.objects.get(pk=perm)
            if (
                permission.method == ResourcePermission.Method.ALLOW
                and permission.action == action
            ):
                path = permission.permission_path
                regex_pattern = re.compile(path)
                all_resources = ResourceGroup.objects.all()
                resources = list(
                    filter(lambda x: regex_pattern.search(x.path), all_resources)
                )
                resource_list.extend(resources)

        resources_to_exclude = []
        for perm in permissions:
            permission = ResourcePermission.objects.get(pk=perm)
            if (
                permission.method == ResourcePermission.Method.DENY
                and permission.action == action
            ):
                path = permission.permission_path
                regex_pattern = re.compile(path)
                all_resources = ResourceGroup.objects.all()
                resources = list(
                    filter(lambda x: regex_pattern.search(x.path), all_resources)
                )
                resources_to_exclude.extend(resources)

        final_resource_list = []
        for resource in resource_list:
            if resource not in resources_to_exclude:
                final_resource_list.append(resource)

        return resource_list

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for instance in serializer.data:
                instance_obj = ResourceGroup.objects.get(id=instance["id"])
                instance["data"] = (
                    json.loads(instance_obj.data[0]["_value"])
                    if instance_obj.data
                    else None
                )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for instance in serializer.data:
            instance_obj = ResourceGroup.objects.get(id=instance["id"])
            instance["data"] = instance_obj.data

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["PATCH"],
    )
    def data(self, request, pk=None):
        new_data = request.data
        resource = self.get_queryset().get(id=pk)
        resource.store_data(new_data)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["GET"],
    )
    def retrieve_data(self, request, pk=None):
        start = request.query_params.get("start", None)
        resource = self.get_queryset().get(id=pk)
        data = resource.get_data(start)
        return Response(data)


class ResourcePermissionViewSet(ModelViewSet):
    queryset = ResourcePermission.objects.all()
    serializer_class = ResourcePermissionSerializer
    permission_classes = (IsSuperUser,)


class TelemetryViewset(ViewSet):
    @action(detail=False, methods=["POST"])
    def query(self, request):
        data = request.data
        start = data.get("start", None)
        end = data.get("end", None)
        # key = data.get("key", None)
        query = QUERIES.START_END_KEY.format(start=start, end=end)
        result = execute_query(query)
        return Response(result)
    
    @action(detail=False, methods=["POST"])
    def insert(self, request):
        data = request.data
        print(data, flush=True)
        ts = data.get("ts")
        key = data.get("key")
        long_v = data.get("long_v", 'null')
        dbl_v = data.get("double_v", 'null')
        str_v = data.get("str_v", 'null')
        bool_v = data.get("bool_v", 'null')
        json_v = data.get("json_v", 'null')

        query = """
        INSERT INTO ts_kv (entity_id, ts, key, long_v, dbl_v, str_v, bool_v, json_v)
        Values ('ead91e90-2e4a-11ef-b1c5-0d3ef55d4ec9', {ts}, {key}, {long_v}, {dbl_v}, '{str_v}', {bool_v}, '{json_v}');
        """.format(
            ts=ts, key=key, long_v=long_v, dbl_v=dbl_v, str_v=str_v, bool_v=bool_v, json_v=json_v
        )
        execute_query(query)
        return Response("ok")
    
class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")
router.register(r"permissions", ResourcePermissionViewSet, basename="permission")
router.register(r"telemetry", TelemetryViewset, basename="telemetry")
