from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

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
from apps.flow.mappings import ITEM_MAPS
from apps.flow.parsers import MultiPartJSONParser
from apps.common.exceptions import bad_request


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

    @action(detail=False, methods=["post"])
    def logs(self, request):
        data = request.data
        flow_id = data.pop("flow")[0]
        timestamp_prefix = data.pop("timestamp_prefix")[0].strip("/")

        flow = get_object_or_404(Flow, pk=flow_id)
        flow_prefix = flow.prefix.full_name
        archive_prefix = (
            flow_prefix.replace(ITEM_TYPE.FLOW.value, ITEM_TYPE.ARCHIVES.value, 1)
            + f"/{flow.name}/logs/{timestamp_prefix}"
        )

        res_prefix = None
        prefixes = archive_prefix.split("/")

        for prefix in prefixes:
            res_prefix = Prefix.objects.get_or_create(name=prefix, parent=res_prefix)[0]

        data["prefix"] = res_prefix.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def artifacts(self, request):
        data = request.data
        flow_id = data.pop("flow")[0]

        flow = get_object_or_404(Flow, pk=flow_id)
        flow_prefix = flow.prefix.full_name
        archive_prefix = (
            flow_prefix.replace(ITEM_TYPE.FLOW.value, ITEM_TYPE.ARCHIVES.value, 1)
            + f"/{flow.name}/artifacts"
        )

        res_prefix = None
        prefixes = archive_prefix.split("/")

        for prefix in prefixes:
            res_prefix = Prefix.objects.get_or_create(name=prefix, parent=res_prefix)[0]

        data["prefix"] = res_prefix.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

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


class SearchViewSet(ViewSet):
    @action(detail=False, methods=["POST"])
    def items(self, request):
        item_type = request.query_params.get("type", None)

        if item_type is None or item_type not in (item.value for item in ITEM_TYPE):
            raise bad_request

        query: str = request.data.get("query", None)
        if query is None:
            raise bad_request

        query = query.strip()

        results = []

        if query.startswith("prefix:"):
            query = query.replace("prefix:", "")
            query = query.strip("/")

            root_prefix = Prefix.objects.get(name=item_type, parent=None)
            res_prefix = [root_prefix]
            prefixes = []
            temp_prefix = root_prefix

            if "/" in query:
                prefixes = query.split("/")
            elif len(query) > 0:
                prefixes = [query]

            for index, prefix in enumerate(prefixes):
                if index == (len(prefixes) - 1):
                    res_prefix = Prefix.objects.filter(
                        name__icontains=prefix, parent=temp_prefix
                    )
                else:
                    temp_prefix = Prefix.objects.get(name=prefix, parent=temp_prefix)
                    if temp_prefix is None:
                        res_prefix = []
                        break

            res_prefix = list(res_prefix)

            for prefix in res_prefix:
                results += ITEM_MAPS[item_type]["model"].objects.filter(prefix=prefix)
                res_prefix.extend(prefix.first_childs)

        else:
            results = ITEM_MAPS[item_type]["model"].objects.filter(
                name__icontains=query
            )

        serializer = ITEM_MAPS[item_type]["serializer"](results, many=True)

        return Response(serializer.data)
