from datetime import datetime
import re
import json
import pytz
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAuthenticated

from apps.resource.models import ResourceGroup, ResourcePermission
from apps.resource.serializers import (
    ResourceGroupSerializer,
    ResourcePermissionSerializer,
)
from apps.common.permission import IsSuperUser
from apps.resource.utils import get_action
from rest_framework.views import APIView

from config import const
from influx.connect import InfluxDB

influxdb = InfluxDB()

class ResourceViewSet(ModelViewSet):
    serializer_class = ResourceGroupSerializer
    permission_classes = (IsAuthenticated,)

    # TODO: Optimize the query to get the resources using parent-child relationship
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ResourceGroup.objects.all()
        permissions = user.get_resource_permissions()

        action = get_action(self.action)
        resource_list = []
        for perm in permissions:
            permission = ResourcePermission.objects.get(pk=perm)
            if (
                permission.method == ResourcePermission.Method.ALLOW
                and permission.action == action
            ):
                path = permission.permission_path
                regex_pattern = re.compile(path)
                all_resources = ResourceGroup.objects.all()
                resources = list(
                    filter(lambda x: regex_pattern.search(x.path), all_resources)
                )
                resource_list.extend(resources)

        resources_to_exclude = []
        for perm in permissions:
            permission = ResourcePermission.objects.get(pk=perm)
            if (
                permission.method == ResourcePermission.Method.DENY
                and permission.action == action
            ):
                path = permission.permission_path
                regex_pattern = re.compile(path)
                all_resources = ResourceGroup.objects.all()
                resources = list(
                    filter(lambda x: regex_pattern.search(x.path), all_resources)
                )
                resources_to_exclude.extend(resources)

        final_resource_list = []
        for resource in resource_list:
            if resource not in resources_to_exclude:
                final_resource_list.append(resource)

        return resource_list

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for instance in serializer.data:
                instance_obj = ResourceGroup.objects.get(id=instance["id"])
                instance["data"] = (
                    json.loads(instance_obj.data[0]["_value"])
                    if instance_obj.data
                    else None
                )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for instance in serializer.data:
            instance_obj = ResourceGroup.objects.get(id=instance["id"])
            instance["data"] = instance_obj.data
        return Response(serializer.data)


class ResourcePermissionViewSet(ModelViewSet):
    queryset = ResourcePermission.objects.all()
    serializer_class = ResourcePermissionSerializer
    permission_classes = (IsSuperUser,)


class InfluxStorage(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            measurement = data["measurement"]
            non_timeseries_data = [
                {key: value}
                for key, value in data.items()
                if key not in ["measurement", "kpis"]
            ]
            kpis = data.get("kpis", [])
            print(kpis, non_timeseries_data)
            if not isinstance(kpis, list):
                raise ValueError("kpis should be a list of dictionaries")

            for kpi_data in kpis:
                kpi = kpi_data.get("kpi")
                values = kpi_data.get("values")
                times = kpi_data.get("time")

                if not all([kpi, values, times]):
                    raise ValueError(
                        "Each kpi entry should have 'kpi', 'values', and 'time' keys."
                    )

                if len(values) != len(times):
                    raise ValueError(
                        "Lengths of 'values' and 'time' lists should be the same."
                    )
                print('hehe1')
                for value, time in zip(values, times):
                    data_point = {
                        "measurement": measurement,
                        "kpi": kpi,
                        "value": value,
                        "time": time,
                    }
                    print('hehe2', data_point)
                    influxdb.write(data_point)

            if non_timeseries_data:
                influxdb.write(
                    {
                        "measurement": measurement,
                        "non_timeseries_data": non_timeseries_data,
                    }
                )

            return Response(
                {"message": "Data stored successfully"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        try:
            measurement_name = request.data.get("measurement", "huihui")
            time = request.data.get("time", "100h")
            query = f'from(bucket: "{const.INFLUXDB_BUCKET}") |> range(start: -{time}) |> filter(fn: (r) => r["_measurement"] == "{measurement_name}")'
            data = influxdb.get_data(query)

            fixed_timestamp = datetime(year=2024, month=4, day=1, hour=0, minute=0, second=0, tzinfo=pytz.UTC)
            fixed_time_query = f'from(bucket: "{const.INFLUXDB_BUCKET}") |> range(start: {fixed_timestamp.isoformat()}) |> filter(fn: (r) => r["_measurement"] == "{measurement_name}")'
            non_timeseries_data = influxdb.get_data(fixed_time_query)

            transformed_data = {
                "measurement": measurement_name,
                "kpis": [],
            }

            for entry in data:
                kpi_name = entry["_field"]
                values = entry["_value"]
                time = entry["_time"]

                transformed_data["kpis"].append({
                    "kpi": kpi_name,
                    "values": values,
                    "time": time,
                })
            
            for entry in non_timeseries_data:
                kpi_name = entry["_field"]
                values = entry["_value"]

                transformed_data[kpi_name]=values

            return Response(transformed_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")
router.register(r"permissions", ResourcePermissionViewSet, basename="permission")
