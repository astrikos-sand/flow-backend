from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.shortcuts import get_object_or_404

from apps.flow.serializers import (
    ConnectionSerializer,
    FlowSerializer,
    BaseNodePolymorphicSerializer,
)
from apps.flow.models import Flow


class DataTransferManager(ViewSet):
    @action(methods=["post"], detail=False)
    def duplicate(self, request):
        flow_id = request.data.get("flow")
        flow = get_object_or_404(Flow, id=flow_id)

        nodes = flow.nodes.all()
        duplicate_flow = None

        try:
            flow_serializer = FlowSerializer(
                data={
                    "name": f"{flow.name} (copy)",
                    "description": flow.description,
                    "lib": flow.lib.id,
                }
            )
            flow_serializer.is_valid(raise_exception=True)
            flow_serializer.save()
            duplicate_flow = flow_serializer.instance

            all_connections_in = []
            input_old_to_new = {}
            output_old_to_new = {}

            for node in nodes:
                node_data = node.export_data()
                node_data["flow"] = duplicate_flow.id
                old_input_slots = node_data.pop("input_slots")
                old_output_slots = node_data.pop("output_slots")
                connections_in = node_data.pop("connections_in")
                all_connections_in.extend(connections_in)

                input_slots_dict = {}
                for slot in old_input_slots:
                    input_slots_dict[slot.name] = str(slot.id)

                output_slots_dict = {}
                for slot in old_output_slots:
                    output_slots_dict[slot.name] = str(slot.id)

                node_serializer = BaseNodePolymorphicSerializer(data=node_data)
                node_serializer.is_valid(raise_exception=True)
                node_serializer.save()

                duplicate_node = node_serializer.instance
                input_slots = duplicate_node.input_slots
                output_slots = duplicate_node.output_slots

                for slot in input_slots:
                    old_id = input_slots_dict[slot.name]
                    input_old_to_new[old_id] = str(slot.id)

                for slot in output_slots:
                    old_id = output_slots_dict[slot.name]
                    output_old_to_new[old_id] = str(slot.id)

            for connection in all_connections_in:
                duplicate_connection = {
                    "from_slot": output_old_to_new[str(connection.from_slot.id)],
                    "to_slot": input_old_to_new[str(connection.to_slot.id)],
                }
                connection_serializer = ConnectionSerializer(data=duplicate_connection)
                connection_serializer.is_valid(raise_exception=True)
                connection_serializer.save()

        except Exception as e:
            if duplicate_flow:
                duplicate_flow.delete()
            print(e, flush=True)
            return Response(
                {"success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"success": True})

    @action(methods=["post"], detail=False, url_path="import")
    def import_data(self, request):
        pass

    @action(methods=["post"], detail=False, url_path="export")
    def export_data(self, request):
        pass
