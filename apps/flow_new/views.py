from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.request import Request

from apps.flow_new.models import Tag, FileArchive
from apps.flow_new.serializers import TagSerializer, FileArchiveSerializer
from apps.flow_new.mappings import ITEM_MAPS
from apps.common.exceptions import bad_request


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=False, methods=["POST"])
    def search(self, request: Request):
        names = request.data.get("names", [])
        exact_match = request.data.get("exact_match", False)

        tags = Tag.objects.filter(
            name__in=names,
        )

        temp = []
        for tag in tags:
            temp.append(tag)
            temp.extend(tag.children)

        tags = list(set(temp))

        items = []
        for tag in tags:
            items.extend(tag.items.all())

        items = list(set(items))

        result = []
        for item in items:
            serializer = ITEM_MAPS[item.item_type]["serializer"]
            serializer = serializer(item)
            if exact_match and item.match_tags(names):
                result.append(serializer.data)
            elif not exact_match:
                result.append(serializer.data)

        return Response(result)

    @action(detail=False, methods=["get"])
    def get_parent_tag(self, request: Request):
        item_type = request.query_params.get("type", None)
        if not item_type or item_type not in ITEM_MAPS:
            raise bad_request

        tag = Tag.objects.get(
            name=item_type,
            parent=None,
        )
        serializer = TagSerializer(tag)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def organized_tags(self, request: Request, pk: str):
        tags = Tag.objects.filter(parent=pk)
        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data)


class FileArchiveViewSet(ModelViewSet):
    queryset = FileArchive.objects.all()
    serializer_class = FileArchiveSerializer


router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"archives", FileArchiveViewSet)
