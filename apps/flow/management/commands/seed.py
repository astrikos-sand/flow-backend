from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from config.const import BASE_DIR
from apps.flow.enums import ITEM_TYPE
from apps.flow.models import Prefix, FunctionDefinition
from apps.flow.serializers import FunctionDefinitionSerializer
from apps.flow.enums import ATTACHMENT_TYPE


def create_default_functions():
    root_prefix = Prefix.objects.get(name=ITEM_TYPE.FUNCTION.value, parent=None)
    default_prefix = Prefix.objects.get_or_create(name="default", parent=root_prefix)[0]
    utils_prefix = Prefix.objects.get_or_create(name="utils", parent=default_prefix)[0]

    functions = [
        {
            "name": "_convert_csv_content_to_df",
            "code": "convert_csv_content_to_df.py",
            "fields": [
                {
                    "name": "csv_content",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "df",
                    "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                },
            ],
        },
        {
            "name": "_df_to_csv_content",
            "code": "df_to_csv_content.py",
            "fields": [
                {
                    "name": "df",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "csv_content",
                    "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                },
            ],
        },
        {
            "name": "_download_file_content",
            "code": "download_file_content.py",
            "fields": [
                {
                    "name": "url",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "content",
                    "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                },
            ],
        },
        {
            "name": "_pickle_dump",
            "code": "pickle_dump.py",
            "fields": [
                {
                    "name": "python_obj",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "dumped_content",
                    "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                },
            ],
        },
        {
            "name": "_pickle_load",
            "code": "pickle_load.py",
            "fields": [
                {
                    "name": "dumped_content",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "python_obj",
                    "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                },
            ],
        },
        {
            "name": "_save_file_content",
            "code": "save_file_content.py",
            "fields": [
                {
                    "name": "content",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "name",
                    "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                },
                {
                    "name": "file_url",
                    "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                },
            ],
        },
    ]

    dir_path = BASE_DIR / "ml-utilities" / "functions"

    for function in functions:
        file_path = dir_path / function["code"]

        with open(file_path, "rb") as file:
            data = {
                **function,
                "code": ContentFile(file.read(), name=function["code"]),
                "prefix": utils_prefix.id,
            }
            try:
                FunctionDefinition.objects.get(
                    name=function["name"], prefix=utils_prefix
                )
            except FunctionDefinition.DoesNotExist:
                serializer = FunctionDefinitionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        for item_type in ITEM_TYPE:
            root, _ = Prefix.objects.get_or_create(name=item_type.value, parent=None)
            Prefix.objects.get_or_create(name="miscellaneous", parent=root)

        create_default_functions()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
