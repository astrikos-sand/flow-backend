import json
import re

from django.db import models
from django.core.validators import RegexValidator

from treebeard.ns_tree import NS_Node

from apps.common.models import BaseModel
from apps.iam.models import IAMUser
import config.const as const

from influx import influx


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
        query = f'from(bucket: "{const.INFLUXDB_BUCKET}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "{self.path}")'
        result = influx.get_data(query)
        return result

    def store_data(self, data: dict) -> None:
        influx.write({"measurement": self.path, "value": json.dumps(data)})

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
