from django.db import models

from apps.common.models import BaseModel


class Prefix(BaseModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    @property
    def full_name(self) -> str:
        return f"{self.parent.full_name}/{self.name}" if self.parent else self.name

    @property
    def first_childs(self) -> list["Prefix"]:
        return list(self.children.all())

    def __str__(self):
        return self.full_name

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
