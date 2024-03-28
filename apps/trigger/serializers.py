from rest_framework import serializers

import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from apps.trigger.models import WebHookTrigger, PeriodicTrigger
from apps.flow.models import BaseNode


class WebHookTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebHookTrigger
        fields = "__all__"


class PeriodicTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTrigger
        fields = "__all__"

    def create(self, validated_data):
        scheduler: PeriodicTrigger = PeriodicTrigger.objects.create(**validated_data)
        node: BaseNode = scheduler.node

        task_name = f"{node.flow_file.name} - {node.id}"
        task = "apps.trigger.tasks.periodic_task"

        if scheduler.scheduler_type is PeriodicTrigger.SCHDULER_TYPE.INTERVAL:
            task_interval, _ = IntervalSchedule.objects.get_or_create(
                every=scheduler.duration.seconds, period=IntervalSchedule.SECONDS
            )

            task = PeriodicTask.objects.create(
                interval=task_interval,
                name=task_name,
                task=task,
                kwargs=json.dumps({"node": node, "context": self.context}),
            )
        else:
            task_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=scheduler.minute,
                hour=scheduler.hour,
                day_of_week=scheduler.day_of_week,
                day_of_month=scheduler.day_of_month,
                month_of_year=scheduler.month_of_year,
                timezone=scheduler.timezone,
            )

            task = PeriodicTask.objects.create(
                crontab=task_schedule,
                name=task_name,
                task=task,
                kwargs=json.dumps({"node": node, "context": self.context}),
            )

        return scheduler
