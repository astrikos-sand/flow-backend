import pika
import threading


class QueueListener(threading.Thread):
    def __init__(self, queue_name: str):
        threading.Thread.__init__(self)
        credentials = pika.PlainCredentials("root", "root")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost", credentials=credentials, port="5672", virtual_host="/"
            )
        )
        self.channel = connection.channel()
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.start_consuming()
