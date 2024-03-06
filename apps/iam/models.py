from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator

from apps.common.models import BaseModel
from apps.iam.managers import IAMUserManager


class IAMUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        unique=True,
        max_length=100,
        validators=[
            RegexValidator(r"^[a-zA-Z0-9_-]{3,}$"),
        ],
    )
    is_active = models.BooleanField(default=True)
    policies = models.ManyToManyField("Policy", related_name="users")
    roles = models.ManyToManyField("Role", related_name="users")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = IAMUserManager()

    def __str__(self) -> str:
        return self.username

    @property
    def is_staff(self):
        return self.is_active


class ResourcePermission(BaseModel):
    class Action(models.TextChoices):
        READ = "r", "read"
        WRITE = "w", "write"
        UPDATE = "u", "update"
        DELETE = "d", "delete"

    action = models.CharField(choices=Action)
    path = models.CharField()

    def __str__(self) -> str:
        return f"{self.path} ({self.action})"

    class Meta:
        ordering = (
            "path",
            "action",
        )
        unique_together = (
            "path",
            "action",
        )

    @staticmethod
    def create_default_permissions(path: str) -> tuple["ResourcePermission"]:
        return tuple(
            [
                ResourcePermission(action=action, path=path)
                for action in ResourcePermission.Action.values
            ]
        )


class PolicyResourcePermissionRelation(BaseModel):
    policy = models.ForeignKey("Policy", on_delete=models.CASCADE)
    permission = models.ForeignKey("ResourcePermission", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "policy",
            "permission",
        )

    def save(self, *args, **kwargs):
        path = self.policy.path
        if path is not None and path != self.permission.path:
            raise ValueError(
                "A policy should be attached to permission with the same path"
            )
        super().save(*args, **kwargs)


class Policy(BaseModel):
    class Method(models.TextChoices):
        ALLOW = True, "allow"
        DENY = False, "deny"

    permissions = models.ManyToManyField(
        ResourcePermission,
        through="PolicyResourcePermissionRelation",
        related_name="policies",
    )
    method = models.BooleanField(choices=Method)

    @property
    def short_name(self) -> str:
        permissions = self.permissions.all()
        actions = "".join([permission.action for permission in permissions])
        return actions

    @property
    def path(self) -> str | None:
        if self.permissions.exists():
            return self.permissions.first().path
        return None

    def __str__(self) -> str:
        return f"{self.method} {self.short_name} {self.path}"


class Role(BaseModel):
    name = models.CharField(unique=True)
    policies = models.ManyToManyField("Policy", related_name="roles")

    def __str__(self) -> str:
        return self.name
