from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from timezone_field import TimeZoneField
from django_celery_beat import validators
from django_celery_beat.models import crontab_schedule_celery_timezone, PeriodicTask
from datetime import timedelta

from apps.common.models import BaseModel
from apps.flow.models import BaseNode, FlowFile


class Trigger(BaseModel):
    node = models.OneToOneField(BaseNode, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class WebHookTrigger(Trigger):
    pass


class PeriodicTrigger(Trigger):

    class SCHDULER_TYPE(models.TextChoices):
        INTERVAL = "interval", "Interval"
        CRONTAB = "crontab", "Crontab"

    scheduler_type = models.CharField(
        choices=SCHDULER_TYPE.choices, default=SCHDULER_TYPE.INTERVAL, max_length=10
    )

    flow_file = models.ForeignKey(
        FlowFile,
        on_delete=models.CASCADE,
        related_name="periodic_triggers",
        null=True,
        blank=True,
    )

    task = models.OneToOneField(
        PeriodicTask, on_delete=models.CASCADE, null=True, blank=True
    )

    # interval scheduler
    duration = models.DurationField(
        default=timedelta(minutes=1), verbose_name=_("Duration")
    )

    # crontab scheduler
    minute = models.CharField(
        max_length=60 * 4,
        null=True,
        blank=True,
        default="*",
        verbose_name=_("Minute(s)"),
        help_text=_('Cron Minutes to Run. Use "*" for "all". (Example: "0,30")'),
        validators=[validators.minute_validator],
    )

    hour = models.CharField(
        max_length=24 * 4,
        default="*",
        null=True,
        blank=True,
        verbose_name=_("Hour(s)"),
        help_text=_('Cron Hours to Run. Use "*" for "all". (Example: "8,20")'),
        validators=[validators.hour_validator],
    )

    day_of_month = models.CharField(
        max_length=31 * 4,
        default="*",
        null=True,
        blank=True,
        verbose_name=_("Day(s) Of The Month"),
        help_text=_(
            'Cron Days Of The Month to Run. Use "*" for "all". ' '(Example: "1,15")'
        ),
        validators=[validators.day_of_month_validator],
    )

    month_of_year = models.CharField(
        max_length=64,
        default="*",
        null=True,
        blank=True,
        verbose_name=_("Month(s) Of The Year"),
        help_text=_(
            'Cron Months (1-12) Of The Year to Run. Use "*" for "all". '
            '(Example: "1,12")'
        ),
        validators=[validators.month_of_year_validator],
    )

    day_of_week = models.CharField(
        max_length=64,
        default="*",
        null=True,
        blank=True,
        verbose_name=_("Day(s) Of The Week"),
        help_text=_(
            'Cron Days Of The Week to Run. Use "*" for "all", Sunday '
            'is 0 or 7, Monday is 1. (Example: "0,5")'
        ),
        validators=[validators.day_of_week_validator],
    )

    timezone = TimeZoneField(
        default=crontab_schedule_celery_timezone,
        use_pytz=False,
        null=True,
        blank=True,
        verbose_name=_("Cron Timezone"),
        help_text=_("Timezone to Run the Cron Schedule on. Default is UTC."),
    )
