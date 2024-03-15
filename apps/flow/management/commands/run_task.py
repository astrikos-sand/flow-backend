from django.core.management.base import BaseCommand
from apps.flow.models import BaseNode
from apps.flow.runtime.tasks import execute_flow


class Command(BaseCommand):
    help = "Run Task for a file"

    def add_arguments(self, parser):
        parser.add_argument("file_id", type=str)

    def handle(self, *args, **options):
        uuid = options.get("file_id", None)
        result = execute_flow(uuid)
        print(result)
