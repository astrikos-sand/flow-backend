from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.flow.models import FileArchive, Dependency, Prefix
from apps.flow.serializers import (
    FileArchiveSerializer,
    DependencySerializer,
    PrefixSerializer,
)


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


class FileArchiveViewSet(ModelViewSet):
    queryset = FileArchive.objects.all()
    serializer_class = FileArchiveSerializer


class DependencyViewSet(ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer
