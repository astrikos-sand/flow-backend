from django.db import models

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel
from apps.flow_new.enums import ITEM_TYPE


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
        def get_all_children(tag):
            children = list(Tag.objects.filter(parent=tag))
            for child in children:
                children.extend(get_all_children(child))
            return children

        return get_all_children(self)

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


# TODO: Dynamic enums (use ns_node for tags)
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


class FileArchive(BaseModelWithTag):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return f"{self.name}"

    @property
    def item_type(self) -> str:
        return ITEM_TYPE.ARCHIVES.value

    @property
    def url(self):
        return self.file.url


class Dependency(BaseModelWithTag):
    name = models.CharField(max_length=100, unique=True)
    requirements = models.FileField(upload_to="flow/dependencies/")

    @property
    def item_type(self) -> str:
        return ITEM_TYPE.DEPENDENCY.value

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Dependency"
        verbose_name_plural = "Dependencies"


class Flow(BaseModelWithTag):
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
        if self.scope:
            return f"{self.scope}/{self.name}"
        return f"{self.name}"

    @property
    def item_type(self) -> str:
        return ITEM_TYPE.FLOW.value
