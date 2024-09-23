from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from apps.flow.models import FileArchive, Dependency, Prefix, Flow, FunctionDefinition
from apps.flow.serializers import (
    FileArchiveSerializer,
    DependencySerializer,
    PrefixSerializer,
    FlowSerializer,
    BaseNodePolymorphicSerializer,
    FunctionDefinitionSerializer,
)
from apps.flow.runtime.worker import submit_task, create_environment
from apps.flow.enums import ITEM_TYPE
from apps.flow.parsers import MultiPartJSONParser


class PrefixViewSet(ModelViewSet):
    queryset = Prefix.objects.all()
    serializer_class = PrefixSerializer

    @action(detail=False, methods=["get"], url_path="page-data")
    def page_data(self, request):
        query_params = request.query_params
        parent = query_params.get("parent", None)
        queryset = self.get_queryset().filter(parent=parent)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FlowViewSet(ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    @action(detail=False, methods=["get"], url_path="page-data")
    def page_data(self, request):
        query_params = request.query_params
        parent = query_params.get("parent", None)

        if parent is None:
            parent = Prefix.objects.get(name=ITEM_TYPE.FLOW.value)

        items = self.get_queryset().filter(prefix=parent)
        serializer = self.get_serializer(items, many=True)

        prefixes = Prefix.objects.filter(parent=parent)

        data = {
            "tree": PrefixSerializer(prefixes, many=True).data,
            "items": serializer.data,
        }
        return Response(data)

    @action(detail=True, methods=["POST"])
    def execute(self, request: Request, pk: str):
        flow = get_object_or_404(Flow, pk=pk)
        data = {
            "flow": FlowSerializer(flow).data,
            "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
            "lib": DependencySerializer(flow.lib).data,
        }
        result = submit_task(data)
        return Response(result)

    @action(detail=True, methods=["GET"])
    def nodes(self, request: Request, pk: str):
        flow = get_object_or_404(Flow, pk=pk)
        data = {
            "flow": FlowSerializer(flow).data,
            "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
        }
        return Response(data)


class FileArchiveViewSet(ModelViewSet):
    queryset = FileArchive.objects.all()
    serializer_class = FileArchiveSerializer

    @action(detail=False, methods=["get"], url_path="page-data")
    def page_data(self, request):
        query_params = request.query_params
        parent = query_params.get("parent", None)

        if parent is None:
            parent = Prefix.objects.get(name=ITEM_TYPE.ARCHIVES.value)

        items = self.get_queryset().filter(prefix=parent)
        serializer = self.get_serializer(items, many=True)

        prefixes = Prefix.objects.filter(parent=parent)

        data = {
            "tree": PrefixSerializer(prefixes, many=True).data,
            "items": serializer.data,
        }
        return Response(data)


class DependencyViewSet(ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
        create_environment(data)
        return response

    @action(detail=False, methods=["get"], url_path="page-data")
    def page_data(self, request):
        query_params = request.query_params
        parent = query_params.get("parent", None)

        if parent is None:
            parent = Prefix.objects.get(name=ITEM_TYPE.DEPENDENCY.value)

        items = self.get_queryset().filter(prefix=parent)
        serializer = self.get_serializer(items, many=True)

        prefixes = Prefix.objects.filter(parent=parent)

        data = {
            "tree": PrefixSerializer(prefixes, many=True).data,
            "items": serializer.data,
        }
        return Response(data)


class FunctionDefinitionViewSet(ModelViewSet):
    queryset = FunctionDefinition.objects.all()
    serializer_class = FunctionDefinitionSerializer
    parser_classes = [MultiPartJSONParser]

    @action(detail=False, methods=["get"], url_path="page-data")
    def page_data(self, request):
        query_params = request.query_params
        parent = query_params.get("parent", None)

        if parent is None:
            parent = Prefix.objects.get(name=ITEM_TYPE.FUNCTION.value)

        items = self.get_queryset().filter(prefix=parent)
        serializer = self.get_serializer(items, many=True)

        prefixes = Prefix.objects.filter(parent=parent)

        data = {
            "tree": PrefixSerializer(prefixes, many=True).data,
            "items": serializer.data,
        }
        return Response(data)
