import json

from django.core.serializers.json import DjangoJSONEncoder

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


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        exclude = (
            "created_at",
            "updated_at",
        )


class WebHookTriggerSerializer(TriggerSerializer):
    class Meta(TriggerSerializer.Meta):
        model = WebHookTrigger


class IntervalSchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"

    def create(self, validated_data):
        duration = validated_data.get("duration", None)

        task_interval, _ = IntervalSchedule.objects.get_or_create(
            every=duration.seconds, period=IntervalSchedule.SECONDS
        )
        return task_interval


class CronTabSchedulerSerializer(serializers.ModelSerializer):
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
        model = CrontabSchedule
        fields = "__all__"

    def _validate_nullable_choice_field(self, value, choices, default=None):
        if not value and value not in choices:
            value = default
        return value

    def validate_timezone(self, value):
        return self._validate_nullable_choice_field(
            value, self.fields["timezone"].choices, self.fields["timezone"].default
        )

    def create(self, validated_data):
        minute = validated_data.get("minute", None)
        hour = validated_data.get("hour", None)
        day_of_week = validated_data.get("day_of_week", None)
        day_of_month = validated_data.get("day_of_month", None)
        month_of_year = validated_data.get("month_of_year", None)
        timezone = validated_data.get("timezone", None)

        task_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute if minute else "*",
            hour=hour if hour else "*",
            day_of_week=day_of_week if day_of_week else "*",
            day_of_month=day_of_month if day_of_month else "*",
            month_of_year=month_of_year if month_of_year else "*",
            timezone=timezone if timezone else "UTC",
        )

        return task_schedule


class PeriodicTriggerSerializer(TriggerSerializer):
    class Meta(TriggerSerializer.Meta):
        model = PeriodicTrigger

    def validate(self, data: dict):
        scheduler_type = data.get("scheduler_type")
        if scheduler_type not in SCHDULER_TYPE.values:
            raise serializers.ValidationError(
                f"Invalid scheduler type {scheduler_type}"
            )
        return super().validate(data)

    def create(self, validated_data):
        scheduler_type = validated_data.pop("scheduler_type", None)
        target = validated_data.pop("target")

        task_name = f"{target.name} ({scheduler_type})"
        task = "apps.trigger.tasks.periodic_task"

        match scheduler_type:
            case SCHDULER_TYPE.INTERVAL.value:
                task_interval = IntervalSchedulerSerializer(data=validated_data)
                task_interval.is_valid(raise_exception=True)
                task_interval = task_interval.save()

                periodic_task = PeriodicTask.objects.create(
                    interval=task_interval,
                    name=task_name,
                    task=task,
                    kwargs=json.dumps({"flow": target}, cls=DjangoJSONEncoder),
                )
            case SCHDULER_TYPE.CRONTAB.value:
                task_schedule = CronTabSchedulerSerializer(data=validated_data)
                task_schedule.is_valid(raise_exception=True)
                task_schedule = task_schedule.save()

                periodic_task = PeriodicTask.objects.create(
                    crontab=task_schedule,
                    name=task_name,
                    task=task,
                    kwargs=json.dumps({"flow": target}, cls=DjangoJSONEncoder),
                )

        scheduler: PeriodicTrigger = PeriodicTrigger.objects.create(
            task=periodic_task, target=target
        )

        return scheduler
