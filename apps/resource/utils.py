from apps.resource.models import ResourcePermission


def get_action(action: str):
    if action == "list":
        return ResourcePermission.Action.READ
    if action == "retrieve":
        return ResourcePermission.Action.READ
    if action == "create":
        return ResourcePermission.Action.WRITE
    if action == "update":
        return ResourcePermission.Action.WRITE
    if action == "partial_update":
        return ResourcePermission.Action.WRITE
    if action == "destroy":
        return ResourcePermission.Action.DELETE
