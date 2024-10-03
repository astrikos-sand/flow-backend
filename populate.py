from apps.flow.models import Flow, FunctionDefinition, FileArchive, Dependency, Prefix
from apps.flow.enums import ITEM_TYPE
from apps.flow.serializers import DependencySerializer
from apps.flow.runtime.worker import create_environment
from rest_framework.renderers import JSONRenderer

flow_root_prefix = Prefix.objects.get(name=ITEM_TYPE.FLOW.value, parent=None)
flow_misc_prefix = Prefix.objects.get(name='miscellaneous', parent=flow_root_prefix)

function_root_prefix = Prefix.objects.get(name=ITEM_TYPE.FUNCTION.value, parent=None)
function_misc_prefix = Prefix.objects.get(name='miscellaneous', parent=function_root_prefix)

dependency_root_prefix = Prefix.objects.get(name=ITEM_TYPE.DEPENDENCY.value, parent=None)
dependency_misc_prefix = Prefix.objects.get(name='miscellaneous', parent=dependency_root_prefix)

file_archive_root_prefix = Prefix.objects.get(name=ITEM_TYPE.ARCHIVES.value, parent=None)
file_archive_misc_prefix = Prefix.objects.get(name='miscellaneous', parent=file_archive_root_prefix)

for flow in Flow.objects.all():
    flow.prefix = flow_misc_prefix
    flow.save()

for function in FunctionDefinition.objects.all():
    function.prefix = function_misc_prefix
    function.save()

for dependency in Dependency.objects.all():
    serializer = DependencySerializer(data={
        'prefix': dependency_misc_prefix.id,
        'name': f"{dependency.name}-cp".lower(),
        'requirements': dependency.requirements
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()

    create_environment(serializer.data)


for file_archive in FileArchive.objects.all():
    file_archive.prefix = file_archive_misc_prefix
    file_archive.save()
