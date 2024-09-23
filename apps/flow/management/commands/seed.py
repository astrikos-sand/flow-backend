from django.core.management.base import BaseCommand

from apps.flow.enums import ITEM_TYPE
from apps.flow.models import Prefix


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        for item_type in ITEM_TYPE:
            root, _ = Prefix.objects.get_or_create(name=item_type.value)
            Prefix.objects.get_or_create(name="miscellaneous", parent=root)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
