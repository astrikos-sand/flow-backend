from rest_framework import serializers

import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from apps.scheduler.models import WebHookScheduler, PeriodicScheduler
from apps.flow.models import BaseNode

class WebHookScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebHookScheduler
        fields = "__all__"

class PeriodicScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicScheduler
        fields = "__all__"
        
    def create(self, validated_data):
        scheduler: PeriodicScheduler = PeriodicScheduler.objects.create(**validated_data)
        node: BaseNode = scheduler.node
        
        task_name = f'{node.flow_file.name} - {node.id}'
        task = 'apps.scheduler.tasks.periodic_task'
        
        if scheduler.scheduler_type is PeriodicScheduler.SCHDULER_TYPE.INTERVAL:
            task_interval, _ = IntervalSchedule.objects.get_or_create(every=scheduler.duration.seconds, period=IntervalSchedule.SECONDS)
            
            task = PeriodicTask.objects.create(
                interval=task_interval,
                name=task_name,
                task=task,
                kwargs=json.dumps({"node": node}),
            )
            
        else:
            task_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=scheduler.minute,
                hour=scheduler.hour,
                day_of_week=scheduler.day_of_week,
                day_of_month=scheduler.day_of_month,
                month_of_year=scheduler.month_of_year,
                timezone = scheduler.timezone
            )
            
            task = PeriodicTask.objects.create(
                crontab=task_schedule,
                name=task_name,
                task=task,
                kwargs=json.dumps({"node": node}),
            )
        
        return scheduler