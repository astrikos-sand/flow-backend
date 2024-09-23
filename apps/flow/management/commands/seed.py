from django.core.management.base import BaseCommand

from apps.flow.enums import ITEM_TYPE


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        for item_type in ITEM_TYPE:
            pass
            # Tag.objects.get_or_create(name=item_type.value)
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
