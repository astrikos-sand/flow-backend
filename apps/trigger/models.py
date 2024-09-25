from django.db import models
from django.utils.translation import gettext_lazy as _

from django_celery_beat.models import PeriodicTask

from apps.flow.models import Flow, BaseModelWithPrefix


class Trigger(BaseModelWithPrefix):
    target = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="%(class)s")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.target.name}"


class WebHookTrigger(Trigger):
    pass


class PeriodicTrigger(Trigger):
    task = models.OneToOneField(
        PeriodicTask, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.target.name} - {self.task.name}"
