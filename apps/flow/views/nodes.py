from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.common.exceptions import bad_request
from apps.flow.models.nodes import Slot
from apps.flow.serializers import (
    BaseNodePolymorphicSerializer,
    ConnectionSerializer,
)
from apps.flow.models import (
    BaseNode,
    Flow,
    Connection,
)


class BaseNodeViewSet(ModelViewSet):
    queryset = BaseNode.objects.all()
    serializer_class = BaseNodePolymorphicSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


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
                node = BaseNode.objects.get(id=node_id)
                node.flow = flow
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
                    and str(exist_conn.from_slot.id) == incoming_conn["source_slot"]
                    and str(exist_conn.to_slot.id) == incoming_conn["target_slot"]
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
            existing_conn_set = set(
                (conn.from_slot.id, conn.to_slot.id) for conn in existing_connections
            )
            for conn in connections_to_create:
                try:
                    from_slot = Slot.objects.get(id=conn["source_slot"])
                    to_slot = Slot.objects.get(id=conn["target_slot"])
                    if (from_slot.id, to_slot.id) not in existing_conn_set:
                        serialized_connections.append(
                            {"from_slot": from_slot.id, "to_slot": to_slot.id}
                        )
                        existing_conn_set.add((from_slot.id, to_slot.id))
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

            if serialized_connections:
                serializer = ConnectionSerializer(
                    data=serialized_connections, many=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(status=status.HTTP_200_OK)
