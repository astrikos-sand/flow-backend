from django.db import models

from apps.flow_new.enums import ITEM_TYPE

from apps.flow_new.models.base import BaseModelWithTag


class FileArchive(BaseModelWithTag):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return f"{self.name}"

    @property
    def item_type(self) -> str:
        return ITEM_TYPE.ARCHIVES

    @property
    def url(self):
        return self.file.url
