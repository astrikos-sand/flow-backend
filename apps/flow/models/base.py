from django.db import models

from apps.flow.models.prefix import BaseModelWithPrefix


class FileArchive(BaseModelWithPrefix):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        if self.prefix:
            return f"{self.prefix.full_name}/{self.name}"
        return self.name

    @property
    def url(self):
        return self.file.url


class Dependency(BaseModelWithPrefix):
    name = models.CharField(max_length=100, unique=True)
    requirements = models.FileField(upload_to="flow/dependencies/")

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
        if self.prefix:
            return f"{self.prefix.full_name}/{self.full_name}"
        return self.full_name

    @property
    def full_name(self):
        if self.scope:
            return f"{self.scope}/{self.name}"
        return f"{self.name}"
