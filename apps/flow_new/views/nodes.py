from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.flow_new.serializers import (
    BaseNodePolymorphicSerializer,
    FlowSerializer,
    DependencySerializer,
    FunctionDefinitionSerializer,
    ConnectionSerializer,
)
from apps.flow_new.models import (
    BaseNode,
    Flow,
    Dependency,
    FunctionDefinition,
    Connection,
)
from apps.flow_new.runtime.worker import submit_task


class FlowViewSet(ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    @action(detail=True, methods=["POST"])
    def execute(self, request: Request, pk: str):
        flow = get_object_or_404(Flow, pk=pk)
        data = {
            "flow": FlowSerializer(flow).data,
            "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
        }
        result = submit_task(data)
        return Response(data)

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
    # TODO: parsing


class ConnectionViewSet(ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
