from django.db import models

from treebeard.ns_tree import NS_Node

from config.strings import MONGODB
from mongodb import db


class ResourceGroup(NS_Node):
    name = models.CharField(max_length=255, null=True, blank=True)
    resource_type = models.CharField(max_length=255)

    """
    use update when moving node from one
    parent to other and object is still in memory
    """

    @property
    def path(self, update: bool = False):
        if hasattr(self, "_cached_path"):
            if update:
                del self._cached_path
            else:
                return self._cached_path

        parent = self.get_parent()
        child_path = f"{self.resource_type}/{self.name}"
        self._cached_path = (
            child_path if parent is None else f"{parent.path}/{child_path}"
        )
        return self._cached_path

    @property
    def data(self) -> dict:
        query = {"resource_type": self.resource_type}
        res = db[MONGODB.resource].find_one(query)
        return res["data"]

    def store_data(self, data: dict) -> None:
        db[MONGODB.resource].insert_one(
            {
                "resource_type": self.resource_type,
                "data": data,
            }
        )

    def __str__(self):
        return f"{self.name}-{self.resource_type} ({self.path})"
