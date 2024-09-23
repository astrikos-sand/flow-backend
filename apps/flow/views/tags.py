from rest_framework.viewsets import ModelViewSet

from apps.flow.models import FileArchive, Dependency
from apps.flow.serializers import (
    FileArchiveSerializer,
    DependencySerializer,
)


class FileArchiveViewSet(ModelViewSet):
    queryset = FileArchive.objects.all()
    serializer_class = FileArchiveSerializer


class DependencyViewSet(ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer
