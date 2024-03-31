import json
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.decorators import action

from apps.flow.models import (
    BaseNode,
    BaseNodeClass,
    Connection,
    FlowFile,
    GenericNodeClass,
)

from apps.flow.serializers import (
    BaseNodeSerializer,
    BaseNodeClassSerializer,
    FlowFileSerializer,
    SlotSerializer,
)

from apps.flow.runtime.worker import submit_task
from apps.flow.serializers import ConnectionSerializer
from apps.common.permission import IsSuperUser


class BaseNodeViewSet(ModelViewSet):
    queryset = BaseNode.objects.all()
    serializer_class = BaseNodeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class BaseNodeClassViewSet(ModelViewSet):
    queryset = BaseNodeClass.objects.all()
    serializer_class = BaseNodeClassSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class FlowFileViewSet(ModelViewSet):
    queryset = FlowFile.objects.all()
    serializer_class = FlowFileSerializer
    permission_classes = (IsSuperUser,)

    @action(
        detail=False,
        methods=["POST"],
    )
    def create_file(self, request):
        name = request.data.get("name", None)
        desc = request.data.get("description", None)
        FlowFile.objects.create(name=name, description=desc)
        return Response(status=status.HTTP_201_CREATED)


class TaskViewSet(ViewSet):

    def create(self, request):
        file_id = request.data.get("file_id", None)
        if file_id is None:
            return Response(
                {"error": "file_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        nodes = BaseNode.objects.filter(flow_file__id=file_id)
        nodes_data = BaseNodeSerializer(
            nodes, many=True, context={"request": request}
        ).data
        try:
            response = submit_task(nodes_data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {"error": str(e)}
            print({"error": str(e)})
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class SaveAPIView(APIView):
    def post(self, request, *args, **kwargs):
        flow_file_id = request.data.get("flow_file_id")
        if not flow_file_id:
            return Response(
                {"error": "Flow file ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            flow_file = FlowFile.objects.get(id=flow_file_id)
        except FlowFile.DoesNotExist:
            return Response(
                {"error": "Flow file not found"}, status=status.HTTP_404_NOT_FOUND
            )

        received_data = request.data
        received_nodes = received_data.get("nodes", [])

        updated_nodes = []
        saved_connections = []
        for node_data in received_nodes:
            node_id = node_data.get("id")
            try:
                node = BaseNode.objects.get(id=node_id, flow_file=flow_file)
            except BaseNode.DoesNotExist:
                continue
            node.position = node_data.get("position")
            node.save()
            updated_nodes.append(node_data)

        incoming_connections = request.data.get("connections", [])
        current_node_ids = [node_data["id"] for node_data in received_nodes]
        existing_connections = Connection.objects.filter(
            source__id__in=current_node_ids, target__id__in=current_node_ids
        )
        connections_to_delete = []

        for existing_connection in existing_connections:
            if not any(
                existing_connection.id == conn.get("id")
                for conn in incoming_connections
            ):
                connections_to_delete.append(existing_connection.id)

        if connections_to_delete:
            Connection.objects.filter(id__in=connections_to_delete).delete()

        nodes_to_delete = BaseNode.objects.filter(flow_file=flow_file).exclude(
            id__in=current_node_ids
        )
        for node_to_delete in nodes_to_delete:
            node_to_delete.delete()

        serializer = ConnectionSerializer(data=incoming_connections, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveCodeFileAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get("name")
            description = request.data.get("description")
            code_file = request.FILES.get("code_file")
            slots_data = json.loads(request.data.get("slots", []))

            if not name:
                return Response(
                    {"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST
                )
            if not code_file:
                return Response(
                    {"error": "Code file is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not slots_data:
                return Response(
                    {"error": "Slots data is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            node_class = GenericNodeClass.objects.create(
                name=name, description=description, code=code_file
            )

            for slot_data in slots_data:
                slot_data["node_class"] = node_class.id
                slot_serializer = SlotSerializer(data=slot_data)
                if slot_serializer.is_valid():
                    slot_serializer.save()
                else:
                    node_class.delete()
                    return Response(
                        slot_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                BaseNodeClassSerializer(node_class).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


router = DefaultRouter()
router.register(r"nodes", BaseNodeViewSet, basename="node")
router.register(r"flows", FlowFileViewSet, basename="flow")
router.register(r"node-classes", BaseNodeClassViewSet, basename="node-class")
router.register(r"tasks", TaskViewSet, basename="task")
