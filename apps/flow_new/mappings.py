from apps.flow_new.enums import ITEM_TYPE

from apps.flow_new.serializers import FileArchiveSerializer
from apps.flow_new.models import FileArchive


ITEM_MAPS = {
    ITEM_TYPE.ARCHIVES: {
        "serializer": FileArchiveSerializer,
        "model": FileArchive,
    },
}
