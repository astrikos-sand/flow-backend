from django.contrib import admin

from apps.flow_new.models import Tag, BaseModelWithTag, FileArchive

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


@admin.register(BaseModelWithTag)
class BaseModelWithTagAdmin(PolymorphicParentModelAdmin):
    base_model = BaseModelWithTag
    child_models = (FileArchive,)


@admin.register(FileArchive)
class FileArchiveAdmin(PolymorphicChildModelAdmin):
    base_model = FileArchive


admin.site.register(Tag)
