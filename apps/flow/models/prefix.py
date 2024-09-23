from django.db import models

from apps.common.models import BaseModel


class Prefix(BaseModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Prefix"
        verbose_name_plural = "Prefixes"
        unique_together = ("name", "parent")


class BaseModelWithPrefix(BaseModel):
    prefix = models.ForeignKey(
        Prefix,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_items",
    )

    class Meta:
        abstract = True
