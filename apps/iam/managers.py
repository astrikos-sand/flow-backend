from django.contrib.auth.models import BaseUserManager


class IAMUserManager(BaseUserManager):
    def _create_user(self, **kwargs):

        username = kwargs.get("username", None)
        if not username:
            raise ValueError("User must have an username")

        password = kwargs.pop("password", None)
        if not password:
            raise ValueError("User must have a password")

        user = self.model(**kwargs)
        user.set_password(password)
        return user

    def create_user(self, **kwargs):
        user = self._create_user(**kwargs)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self._create_user(**kwargs)
        user.is_superuser = True
        user.save()
        return user
