from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.request import Request

from apps.flow_new.models import Tag, FileArchive, BaseModelWithTag
from apps.flow_new.models.base import Flow
from apps.flow_new.serializers import TagSerializer, FileArchiveSerializer
from apps.flow_new.mappings import ITEM_MAPS
from apps.common.exceptions import bad_request
from apps.flow_new.serializers.nodes import FlowSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=False, methods=["POST"])
    def search(self, request: Request):
        names = request.data.get("names", [])
        exact_match = request.data.get("exact_match", False)
        tags = Tag.objects.filter(name__in=names)
        if exact_match:
            tags = tags.filter(name__in=names)
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)

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

    @action(detail=True, methods=["get"])
    def all_children(self, request: Request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)

        def get_all_children(tag):
            children = Tag.objects.filter(parent=tag)
            return [
                {
                    "id": child.id,
                    "name": child.name,
                    "children": get_all_children(child),
                }
                for child in children
            ]

        data = {"id": tag.id, "name": tag.name, "children": get_all_children(tag)}
        return Response(data)


class FileArchiveViewSet(ModelViewSet):
    queryset = FileArchive.objects.all()
    serializer_class = FileArchiveSerializer

    def create(self, request: Request, *args, **kwargs):
        file = request.FILES.get("file")
        filename = request.data.get("filename")
        parent_tag_id = request.data.get("parentTag")
        new_tag_name = request.data.get("newTag")

        parent_tag = get_object_or_404(Tag, id=parent_tag_id)
        new_tag, created = Tag.objects.get_or_create(
            name=new_tag_name, parent=parent_tag
        )

        file_archive = FileArchive.objects.create(name=filename, file=file)
        file_archive.tags.add(new_tag)
        file_archive.save()

        return Response(FileArchiveSerializer(file_archive).data)


class FlowViewSet(ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    def create(self, request: Request, *args, **kwargs):
        flow_data = request.data
        tags_data = flow_data.pop("tags", [])

        flow = Flow.objects.create(**flow_data)
        for tag_data in tags_data:
            parent_tag_id = tag_data.get("parent")
            tag_name = tag_data.get("name")

            parent_tag = get_object_or_404(Tag, id=parent_tag_id)
            tag, created = Tag.objects.get_or_create(name=tag_name, parent=parent_tag)
            flow.tags.add(tag)

        flow.save()

        return Response(FlowSerializer(flow).data)
