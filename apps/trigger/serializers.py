import json

from django.core.serializers.json import DjangoJSONEncoder
from timezone_field.rest_framework import TimeZoneSerializerField

from rest_framework import serializers

from django_celery_beat.models import (
    crontab_schedule_celery_timezone,
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
)

from apps.trigger.models import (
    WebHookTrigger,
    PeriodicTrigger,
    Trigger,
)
from apps.trigger.enums import SCHDULER_TYPE
from apps.flow.enums import ITEM_TYPE
from apps.flow.models.prefix import Prefix


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        exclude = (
            "created_at",
            "updated_at",
        )


class WebHookTriggerSerializer(TriggerSerializer):
    target_name = serializers.CharField(source="target.name", read_only=True)
    copy_command = serializers.CharField(read_only=True)

    class Meta(TriggerSerializer.Meta):
        model = WebHookTrigger

    def create(self, validated_data):
        prefix: Prefix | None = validated_data.get("prefix", None)

        if prefix is None:
            root = Prefix.objects.get(name=ITEM_TYPE.WEBHOOK.value)
            misc_prefix = Prefix.objects.get(name="miscellaneous", parent=root)
            validated_data["prefix"] = misc_prefix
        else:
            if not prefix.full_name.startswith(ITEM_TYPE.WEBHOOK.value):
                raise serializers.ValidationError("Prefix must start with 'webhooks'")

        return super().create(validated_data)


class IntervalSchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = ("every",)

    def create(self, validated_data):
        every = validated_data.pop("every")

        task_interval, _ = IntervalSchedule.objects.get_or_create(
            every=every, period=IntervalSchedule.SECONDS
        )
        return task_interval


class CronTabSchedulerSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField(default=crontab_schedule_celery_timezone)

    class Meta:
        model = CrontabSchedule
        fields = (
            "minute",
            "hour",
            "day_of_week",
            "day_of_month",
            "month_of_year",
            "timezone",
        )

    def create(self, validated_data):
        minute = validated_data.get("minute", "*")
        hour = validated_data.get("hour", "*")
        day_of_week = validated_data.get("day_of_week", "*")
        day_of_month = validated_data.get("day_of_month", "*")
        month_of_year = validated_data.get("month_of_year", "*")
        timezone = validated_data.get("timezone")

        task_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            timezone=timezone,
        )

        return task_schedule


class TaskSerializer(serializers.ModelSerializer):
    interval = IntervalSchedulerSerializer(read_only=True)
    crontab = CronTabSchedulerSerializer(read_only=True)

    class Meta:
        model = PeriodicTask
        fields = (
            "name",
            "interval",
            "crontab",
        )


class PeriodicTriggerSerializer(TriggerSerializer):
    target_name = serializers.CharField(source="target.name", read_only=True)
    interval = IntervalSchedulerSerializer(required=False, write_only=True)
    crontab = CronTabSchedulerSerializer(required=False, write_only=True)
    name = serializers.CharField(write_only=True)

    task = TaskSerializer(read_only=True)

    class Meta(TriggerSerializer.Meta):
        model = PeriodicTrigger

    def create(self, validated_data):
        prefix: Prefix | None = validated_data.get("prefix", None)

        if prefix is None:
            root = Prefix.objects.get(name=ITEM_TYPE.PERIODIC.value)
            misc_prefix = Prefix.objects.get(name="miscellaneous", parent=root)
            validated_data["prefix"] = misc_prefix
        else:
            if not prefix.full_name.startswith(ITEM_TYPE.PERIODIC.value):
                raise serializers.ValidationError("Prefix must start with 'periodic'")

        interval = validated_data.get("interval", None)
        crontab = validated_data.get("crontab", None)

        if not interval and not crontab:
            raise serializers.ValidationError(
                "Interval or Crontab schedule is required."
            )

        target = validated_data.pop("target")

        scheduler_type = (
            SCHDULER_TYPE.INTERVAL.value if interval else SCHDULER_TYPE.CRONTAB.value
        )

        task_name = f"{str(target.id)[:7]}_" + validated_data.pop("name")
        task = "apps.trigger.tasks.periodic_task"

        match scheduler_type:
            case SCHDULER_TYPE.INTERVAL.value:
                task_interval = IntervalSchedulerSerializer(
                    data=validated_data.pop("interval")
                )
                task_interval.is_valid(raise_exception=True)
                task_interval = task_interval.save()

                periodic_task = PeriodicTask.objects.create(
                    interval=task_interval,
                    name=task_name,
                    task=task,
                    kwargs=json.dumps(
                        {"flow_id": str(target.id)}, cls=DjangoJSONEncoder
                    ),
                )
            case SCHDULER_TYPE.CRONTAB.value:
                task_schedule = CronTabSchedulerSerializer(
                    data=validated_data.pop("crontab")
                )
                task_schedule.is_valid(raise_exception=True)
                task_schedule = task_schedule.save()

                periodic_task = PeriodicTask.objects.create(
                    crontab=task_schedule,
                    name=task_name,
                    task=task,
                    kwargs=json.dumps(
                        {"flow_id": str(target.id)}, cls=DjangoJSONEncoder
                    ),
                )

        scheduler: PeriodicTrigger = PeriodicTrigger.objects.create(
            task=periodic_task, target=target, prefix=validated_data["prefix"]
        )

        return scheduler
