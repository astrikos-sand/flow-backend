from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, _):
        return bool(request.user and request.user.is_superuser)
