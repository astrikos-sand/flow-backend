from django.db import models

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel
from apps.flow_new.enums import ITEM_TYPE, ATTACHMENT_TYPE, VALUE_TYPE


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        if self.parent:
            return f"{self.parent.full_name}/{self.name}"
        return self.name

    @property
    def children(self) -> list["Tag"]:
        tags = Tag.objects.filter(parent=self)
        all_children = []
        for tag in tags:
            all_children.append(tag)
            all_children.extend(tag.children)

        return all_children

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        unique_together = ("name", "parent")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["parent"]),
        ]


class BaseModelWithTag(BaseModel, PolymorphicModel):
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )

    # This property should be implemented in all child class
    @property
    def item_type(self) -> str:
        raise NotImplementedError

    def match_tags(self, names: list[str]) -> bool:
        visit = {name: 0 for name in names}

        for tag in self.tags.all():
            tag_splts = tag.full_name.split("/")
            for name in names:
                if name in tag_splts:
                    visit[name] = 1

        return all(visit.values())
