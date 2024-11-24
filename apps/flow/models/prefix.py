from django.db import models

from apps.common.models import BaseModel
from apps.flow.enums import ITEM_TYPE


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

    @property
    def is_default(self) -> bool:
        for item_type in ITEM_TYPE:
            if self.full_name == item_type.value:
                return True
            elif self.full_name == f"{item_type.value}/miscellaneous":
                return True

        return False

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
