import pika


class QueueProducer:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials("root", "root")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost", credentials=credentials, port="5672", virtual_host="/"
            )
        )
        self.channel = connection.channel()

    def publish(self, body):
        self.channel.basic_publish(body=body, exchange="", routing_key="tb_core.9")
