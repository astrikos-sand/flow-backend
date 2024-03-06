from django.contrib.auth.models import BaseUserManager


class IAMUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_superuser = True
        user.save()
        return user
