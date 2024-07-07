from django.core.management.base import BaseCommand

from apps.flow_new.enums import ITEM_TYPE
from apps.flow_new.models import Tag


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        for item_type in ITEM_TYPE:
            Tag.objects.get_or_create(name=item_type.value)
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
