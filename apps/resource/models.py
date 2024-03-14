from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from treebeard.ns_tree import NS_Node
import re

from apps.common.models import BaseModel
from apps.iam.models import IAMUser

from config.strings import MONGODB
from mongodb import db


# Validation could not be done at model level because of the way treebeard works
# Always use serializer to create and update ResourceGroup
class ResourceGroup(NS_Node, BaseModel):
    name = models.CharField(
        max_length=255,
        db_index=True,
        validators=[
            RegexValidator(r"/", inverse_match=True, message="name can't contain '/'"),
        ],
    )
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

    def check_permission(
        self, action: "ResourcePermission.Action", user: "IAMUser"
    ) -> bool:

        # check directly attached policies
        permissions = user.permissions.all()
        for permission in permissions:
            if (
                re.fullmatch(permission.permission_path, self.path)
                and permission.action == action
            ):
                return permission.method == ResourcePermission.Method.ALLOW  # else DENY

        # check roles attached policies
        roles_permissions = user.roles.all().values_list("permissions", flat=True)
        for permission in roles_permissions:
            if (
                re.fullmatch(permission.permission_path, self.path) == self.path
                and permission.action == action
            ):
                return ResourcePermission.Method.ALLOW  # else DENY

        # TODO check group attached policies

        return False

    def __str__(self):
        return f"{self.name} [ {self.resource_type} ] ( {self.path} )"


class ResourcePermission(BaseModel):
    class Method(models.TextChoices):
        ALLOW = "ALLOW", "allow"
        DENY = "DENY", "deny"

    class Action(models.TextChoices):
        READ = "READ", "read"
        WRITE = "WRITE", "write"
        UPDATE = "UPDATE", "update"
        DELETE = "DELETE", "delete"

    name = models.CharField(
        max_length=255, db_index=True, null=True, blank=True, unique=True
    )
    action = models.CharField(choices=Action, max_length=10)
    method = models.CharField(choices=Method, max_length=10)
    path = models.CharField(max_length=255, db_index=True)
    parent_resource = models.ForeignKey(
        ResourceGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attached_policies",
        db_index=True,
    )

    @property
    def permission_path(self) -> str:
        return (
            f"{self.parent_resource.path}/{self.path}"
            if self.parent_resource
            else self.path
        )

    @property
    def long_name(self) -> str:
        return f"{self.method} {self.action} on {self.permission_path}"

    def __str__(self) -> str:
        return f"{self.name} ( {self.long_name} )" if self.name else self.long_name
