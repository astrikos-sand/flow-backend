from apps.flow.enums import ITEM_TYPE

from apps.flow.serializers import FileArchiveSerializer
from apps.flow.models import FileArchive


ITEM_MAPS = {
    ITEM_TYPE.ARCHIVES.value: {
        "serializer": FileArchiveSerializer,
        "model": FileArchive,
    },
}
