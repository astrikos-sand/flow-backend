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
    @property
    def copy_command(self):
        flow_inputs = self.target.inputs
        inputs = {i.name: "<>" for i in flow_inputs}
        import json

        inputs_str = json.dumps({"inputs": inputs})
        backend_url = "http://192.168.0.218:9100"
        return f"curl -X POST {backend_url}/triggers/webhook/{self.id}/execute/ -H \"Content-Type: application/json\" -d '{inputs_str}'"


class PeriodicTrigger(Trigger):
    task = models.OneToOneField(
        PeriodicTask, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.target.name} - {self.task.name}"
