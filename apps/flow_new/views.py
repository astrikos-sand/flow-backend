from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.request import Request

from apps.flow_new.models import Tag, FileArchive, BaseModelWithTag
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
            tag_items = BaseModelWithTag.objects.filter(tags=tag)
            items.extend(tag_items)

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
    def parent_tag(self, request: Request):
        item_type = request.query_params.get("type", None)
        if not item_type or ITEM_MAPS.get(item_type) is None:
            raise bad_request

        tag = get_object_or_404(Tag, name=item_type, parent=None)
        serializer = TagSerializer(tag)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def items(self, request: Request, pk: str):
        if pk is None:
            raise bad_request

        tag = get_object_or_404(Tag, id=pk)
        items = BaseModelWithTag.objects.filter(tags=tag)
        if not items:
            return Response([])

        serializer = ITEM_MAPS[items[0].item_type]["serializer"](items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def organized_tags(self, request: Request):
        parent = request.query_params.get("parent", None)
        tags = Tag.objects.filter(parent=parent)
        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data)


class FileArchiveViewSet(ModelViewSet):
    queryset = FileArchive.objects.all()
    serializer_class = FileArchiveSerializer


router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"archives", FileArchiveViewSet)
