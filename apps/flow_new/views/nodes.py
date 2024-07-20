from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.common.exceptions import bad_request
from apps.flow_new.models.nodes import Slot
from apps.flow_new.serializers import (
    BaseNodePolymorphicSerializer,
    FlowSerializer,
    DependencySerializer,
    FunctionDefinitionSerializer,
    ConnectionSerializer,
)
from apps.flow_new.parsers import MultiPartJSONParser
from apps.flow_new.models import (
    BaseNode,
    Flow,
    Dependency,
    FunctionDefinition,
    Connection,
)
from apps.flow_new.runtime.worker import submit_task
from apps.flow_new.models import Tag


class FlowViewSet(ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    # TODO
    def create(self, request: Request, *args, **kwargs):
        flow_data = request.data
        tags_data = flow_data.pop("tags", [])

        flow_serializer = FlowSerializer(data=flow_data)
        flow_serializer.is_valid(raise_exception=True)
        flow_serializer.save()
        flow = flow_serializer.instance

        for tag_data in tags_data:
            parent_tag_id = tag_data.get("parent")
            tag_name = tag_data.get("name")

            parent_tag = get_object_or_404(Tag, id=parent_tag_id)
            tag, created = Tag.objects.get_or_create(name=tag_name, parent=parent_tag)
            flow.tags.add(tag)

        flow.save()

        return Response(FlowSerializer(flow).data)

    @action(detail=True, methods=["POST"])
    def execute(self, request: Request, pk: str):
        flow = get_object_or_404(Flow, pk=pk)
        data = {
            "flow": FlowSerializer(flow).data,
            "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
        }
        result = submit_task(data)
        return Response(result)

    # TODO: Deletion of node

    # TODO: Complete the implementation
    @action(detail=True, methods=["POST"])
    def update_flow(self, request: Request, pk: str):
        flow = get_object_or_404(Flow, pk=pk)
        data = request.data

        nodes_to_update = data.get("nodes", [])
        slots = []

        # Update the position of the nodes
        for node_data in nodes_to_update:
            node_id = node_data.get("id")
            node = BaseNode.objects.get(id=node_id, flow=flow)
            node.position = node_data.get("position")
            node.save()

        # Update connections
        nodes = flow.nodes.all()
        received_connections = data.get("connections", [])
        input_slot_ids = []

        for node in nodes:
            input_slots = node.input_slots
            for slot in input_slots:
                input_slot_ids.append(slot.id)

        existing_connections = Connection.objects.filter(to_slot__id__in=input_slot_ids)

        connections_to_delete = []

        for existing_connection in existing_connections:
            exist = False
            for received_connection in received_connections:
                pass

        return Response({"message": "Not implemented yet!"})

    # TODO: Complete the implementation
    @action(detail=True, methods=["GET"])
    def nodes(self, request: Request, pk: str):
        flow = get_object_or_404(Flow, pk=pk)
        data = {
            "flow": FlowSerializer(flow).data,
            **FlowSerializer(flow).data,
            "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
        }
        return Response(data)


class DependencyViewSet(ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer


class BaseNodeViewSet(ModelViewSet):
    queryset = BaseNode.objects.all()
    serializer_class = BaseNodePolymorphicSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class FunctionDefinitionViewSet(ModelViewSet):
    queryset = FunctionDefinition.objects.all()
    serializer_class = FunctionDefinitionSerializer
    parser_classes = [MultiPartJSONParser]


class ConnectionViewSet(ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class DynamicFieldsViewSet(ViewSet):
    @action(detail=False, methods=["GET"])
    def node_types(self, request: Request):
        child_node_classes = BaseNode.__subclasses__()
        data = [child_node_class.__name__ for child_node_class in child_node_classes]
        return Response(data)

    @action(detail=False, methods=["GET"])
    def node_fields(self, request: Request):
        node_type = request.query_params.get("node_type", None)
        data = {}

        child_node_classes = BaseNode.__subclasses__()

        for child_node_class in child_node_classes:
            data[child_node_class.__name__] = child_node_class.get_node_fields()

        if node_type is not None:
            return Response(data[node_type])

        return Response(data)

    @action(detail=False, methods=["GET"])
    def form_fields(self, request: Request):
        node_type = request.query_params.get("node_type", None)
        data = {}

        child_node_classes = BaseNode.__subclasses__()

        for child_node_class in child_node_classes:
            if hasattr(child_node_class, "get_form_fields"):
                form_fields = child_node_class.get_form_fields()
                if form_fields:
                    data[child_node_class.__name__] = form_fields

        if node_type:
            if node_type in data:
                return Response(data[node_type])
            else:
                raise bad_request

        return Response(data)


# TODO
class SaveAPIView(APIView):
    def post(self, request, *args, **kwargs):
        flow_id = request.data.get("flow_id")
        if not flow_id:
            return Response(
                {"error": "Flow ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            flow = Flow.objects.get(id=flow_id)
        except Flow.DoesNotExist:
            return Response(
                {"error": "Flow not found"}, status=status.HTTP_404_NOT_FOUND
            )

        received_data = request.data
        received_nodes = received_data.get("nodes", [])

        updated_nodes = []
        for node_data in received_nodes:
            node_id = node_data.get("id")
            try:
                node = BaseNode.objects.get(id=node_id, flow=flow)
                node.position = node_data.get("position")
                node.save()
                updated_nodes.append(node_data)
            except BaseNode.DoesNotExist:
                continue
            except Exception as e:
                return Response(
                    {"error": f"Error updating node {node_id}: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        incoming_connections = request.data.get("connections", [])
        current_node_ids = [node_data["id"] for node_data in received_nodes]
        existing_connections = Connection.objects.filter(
            from_slot__node__id__in=current_node_ids,
            to_slot__node__id__in=current_node_ids,
        )

        connections_to_delete = []
        connections_to_create = incoming_connections.copy()

        for exist_conn in existing_connections:
            exist = False
            for incoming_conn in incoming_connections:
                if (
                    str(exist_conn.from_slot.node.id) == incoming_conn["source"]
                    and str(exist_conn.to_slot.node.id) == incoming_conn["target"]
                    and exist_conn.from_slot.name == incoming_conn["source_slot"]
                    and exist_conn.to_slot.name == incoming_conn["target_slot"]
                ):
                    connections_to_create.remove(incoming_conn)
                    exist = True
                    break

            if not exist:
                connections_to_delete.append(exist_conn.id)

        if connections_to_delete:
            Connection.objects.filter(id__in=connections_to_delete).delete()

        nodes_to_delete = BaseNode.objects.filter(flow=flow).exclude(
            id__in=current_node_ids
        )
        for node_to_delete in nodes_to_delete:
            node_to_delete.delete()

        if connections_to_create:
            serialized_connections = []
            for conn in connections_to_create:
                try:
                    from_slot = Slot.objects.get(id=conn["source_slot"])
                    to_slot = Slot.objects.get(id=conn["target_slot"])
                    serialized_connections.append(
                        {"from_slot": from_slot.id, "to_slot": to_slot.id}
                    )
                except Slot.DoesNotExist:
                    return Response(
                        {"error": f"Slot not found for connection: {conn}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Exception as e:
                    return Response(
                        {"error": f"Error processing connection {conn}: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            serializer = ConnectionSerializer(data=serialized_connections, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
