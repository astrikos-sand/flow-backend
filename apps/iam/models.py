from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.core.validators import RegexValidator

from apps.common.models import BaseModel
from apps.iam.managers import IAMUserManager


class Role(BaseModel):
    name = models.CharField(unique=True, max_length=255)
    permissions = models.ManyToManyField(
        "resource.ResourcePermission", related_name="roles"
    )

    def __str__(self) -> str:
        return self.name


class IAMUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        unique=True,
        max_length=100,
        validators=[
            RegexValidator(r"^[a-zA-Z0-9_-]{3,}$"),
        ],
    )
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        "resource.ResourcePermission", related_name="users", blank=True
    )
    roles = models.ManyToManyField(Role, related_name="users", blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = IAMUserManager()

    def __str__(self) -> str:
        return self.username

    @property
    def is_staff(self):
        return self.is_active
