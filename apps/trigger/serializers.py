from rest_framework import serializers

import json
from django_celery_beat.models import (
    crontab_schedule_celery_timezone,
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
)

from django.core.serializers.json import DjangoJSONEncoder

from apps.trigger.models import WebHookTrigger, PeriodicTrigger
from apps.flow.models import BaseNode
from apps.flow.serializers import BaseNodeSerializer
from apps.trigger.tasks import create_nodes


class WebHookTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebHookTrigger
        fields = "__all__"


class PeriodicTriggerSerializer(serializers.ModelSerializer):
    timezone = serializers.ChoiceField(
        allow_blank=True,
        allow_null=True,
        choices=crontab_schedule_celery_timezone(),
        default="UTC",
        initial="UTC",
        required=False,
        write_only=True,
    )

    class Meta:
        model = PeriodicTrigger
        fields = "__all__"

    def _validate_nullable_choice_field(self, value, choices, default=None):
        if not value and value not in choices:
            value = default
        return value

    def validate_timezone(self, value):
        print("timzone value", value, flush=True)
        return self._validate_nullable_choice_field(
            value, self.fields["timezone"].choices, self.fields["timezone"].default
        )

    def validate(self, data: dict):

        scheduler_type = data.get("scheduler_type")
        if scheduler_type not in PeriodicTrigger.SCHDULER_TYPE.values:
            raise serializers.ValidationError(
                f"Invalid scheduler type {scheduler_type}"
            )
        return super().validate(data)

    def create(self, validated_data):
        node = validated_data.get("node")
        scheduler_type = validated_data.get("scheduler_type", None)
        duration = validated_data.get("duration", None)
        minute = validated_data.get("minute", None)
        hour = validated_data.get("hour", None)
        day_of_week = validated_data.get("day_of_week", None)
        day_of_month = validated_data.get("day_of_month", None)
        month_of_year = validated_data.get("month_of_year", None)
        timezone = validated_data.get("timezone", None)

        task_name = f"{node.flow_file.name} - {node.id}"
        task = "apps.trigger.tasks.periodic_task"

        node_id = node.id
        node_list = []
        create_nodes(node, node_list)
        node_list = BaseNodeSerializer(node_list, many=True, context=self.context).data

        if scheduler_type == PeriodicTrigger.SCHDULER_TYPE.INTERVAL:
            print("inside interval", flush=True)
            task_interval, created = IntervalSchedule.objects.get_or_create(
                every=duration.seconds, period=IntervalSchedule.SECONDS
            )

            print(f"created interval {created}", flush=True)

            periodic_task = PeriodicTask.objects.create(
                interval=task_interval,
                name=task_name,
                task=task,
                kwargs=json.dumps(
                    {"node_id": node.id, "node_list": node_list}, cls=DjangoJSONEncoder
                ),
            )
        elif scheduler_type == PeriodicTrigger.SCHDULER_TYPE.CRONTAB:
            task_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=minute if minute else "*",
                hour=hour if hour else "*",
                day_of_week=day_of_week if day_of_week else "*",
                day_of_month=day_of_month if day_of_month else "*",
                month_of_year=month_of_year if month_of_year else "*",
                timezone=timezone if timezone else "UTC",
            )

            periodic_task = PeriodicTask.objects.create(
                crontab=task_schedule,
                name=task_name,
                task=task,
                kwargs=json.dumps(
                    {"node_id": node_id, "node_list": node_list}, cls=DjangoJSONEncoder
                ),
            )

        scheduler: PeriodicTrigger = PeriodicTrigger.objects.create(
            task=periodic_task, **validated_data
        )

        return scheduler
