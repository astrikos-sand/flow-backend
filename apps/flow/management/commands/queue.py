from django.core.management.base import BaseCommand
from apps.common.tb_queue.listen import QueueListener


class Command(BaseCommand):
    help = "Launches Listener for RabbitMQ"

    def handle(self, *args, **options):
        td = QueueListener(queue_name="tb_core.9")
        td.start()
        self.stdout.write("Started Consumer Thread")
