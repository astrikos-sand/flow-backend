from django.db import models

from apps.flow.models.prefix import BaseModelWithPrefix
from apps.common.models import BaseModel
from apps.flow.enums import Status
from apps.flow.utils import dependency_upload_path, archive_upload_path
from config.storage import OverwriteStorage


class FileArchive(BaseModelWithPrefix):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=archive_upload_path)

    def __str__(self):
        if self.prefix:
            return f"{self.prefix.full_name}/{self.name}"
        return self.name

    @property
    def url(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete()

        return super().delete(*args, **kwargs)


class Dependency(BaseModelWithPrefix):
    name = models.CharField(max_length=100, unique=True)
    requirements = models.FileField(
        upload_to=dependency_upload_path, storage=OverwriteStorage()
    )

    def __str__(self):
        if self.prefix:
            return f"{self.prefix.full_name}/{self.name}"
        return self.name

    class Meta:
        verbose_name = "Dependency"
        verbose_name_plural = "Dependencies"


class Flow(BaseModelWithPrefix):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lib = models.ForeignKey(
        Dependency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="flows",
    )
    scope = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="local_flows",
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        # if self.scope:
        #     return f"{self.scope}/{self.name}"
        if self.prefix:
            return f"{self.prefix.full_name}/{self.name}"
        return f"{self.name}"

    @property
    def inputs(self):
        from apps.flow.models.flow import InputNode

        input = InputNode.objects.filter(flow=self)
        if len(input) > 0:
            slots = input[0].slots.all()

            return slots

        return []

    @property
    def dag_meta_data(self):
        from apps.flow.models.utils import DAGMetaData

        try:
            dag = DAGMetaData.objects.get(flow=self)
            return {"config": dag.config}
        except DAGMetaData.DoesNotExist:
            return {}


class FlowExecution(BaseModel):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="executions")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    container_logs = models.ForeignKey(
        FileArchive,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="flow_execution_container_logs",
    )
    json_logs = models.ForeignKey(
        FileArchive,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="flow_execution_json_logs",
    )
    html_logs = models.ForeignKey(
        FileArchive,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="flow_execution_html_logs",
    )

    @property
    def timestamp(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Execution of {self.flow} at {self.timestamp}"
