from django.db import models

from treebeard.ns_tree import NS_Node

from config.strings import MONGODB
from mongodb import db


class ResourceGroup(NS_Node):
    # TODO: Why the name null is allowed? We are using it in the path
    name = models.CharField(max_length=255, null=True, blank=True)
    resource_type = models.CharField(max_length=255)

    # TODO: path should be unique??

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
        path = self.path + "/"
        res = db[MONGODB.resource].find_one({"path": path})
        if res is None or "data" not in res:
            return {}
        return res["data"]

    def store_data(self, data: dict) -> None:
        paths = self.path.split("/")
        depth = len(paths)
        iter = db[MONGODB.resource]
        path_tracker = ""

        for i in range(0, depth):
            path = paths[i]
            path_tracker += f"{path}/"
            res = iter.find_one({"path": path_tracker})
            if res is None:
                iter.insert_one({"children": [], "path": path_tracker})
                res = iter.find_one({"path": path_tracker})

            children: list = res.get("children", [])
            if (i + 1) < depth:
                if paths[i + 1] not in children:
                    children.append(paths[i + 1])
                    iter.update_one(
                        {"_id": res["_id"]}, {"$set": {"children": children}}
                    )

        current_data = res.get("data", {})
        iter.update_one(
            {"_id": res["_id"]}, {"$set": {"data": {**current_data, **data}}}
        )

    def __str__(self):
        return f"{self.name}-{self.resource_type} ({self.path})"
