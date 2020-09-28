import pika, sys, os, json
import requests
import logging as logger

logger.basicConfig(level=logger.INFO)


class Consumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.host = os.environ.get("MQ_HOST")
        self.queue = os.environ.get("MQ_QUEUE")
        self.receivers = {
            "process_zip": self._handler_process_zip,
            "s3_sync": self._handler_s3_sync,
        }

    def _handler_process_zip(self, payload):
        logger.info("calling file_processor service..")
        requests.post("http://k8-file-processor:5001/process", json=payload)

    def _handler_s3_sync(self, payload):
        logger.info("calling s3_sync service..")

    def on_message_receive(ch, method, properties, body):
        logger.info(" [x] Received ")
        msg = body.decode()
        logger.info(msg)
        try:
            payload = json.loads(msg)
        except:
            logger.error("Error loading json payload")
        else:
            handler = self.receivers.get(payload["type"], None)
            if not handler:
                logger.info("invalid payload type.")
            handler(payload)

        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def connect(self):
        logger.info(f"Connecting to {self.host}")
        try:
            self.connection = pika.SelectConnection(
                parameters=pika.ConnectionParameters(host=self.host),
                on_open_callback=self.on_connection_open,
                on_open_error_callback=self.on_connection_open_error,
                on_close_callback=self.on_connection_closed,
            )
            return self.connection
        except:
            logger.error(f"Error establishing connection to rabbitmq host {self.host}")

    def on_connection_open(self, _unused_connection):
        logger.debug("Connection opened")
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message_receive
        )
        logger.info(" [*] starting receiver..")
        self.channel.start_consuming()

    def on_connection_open_error(self, _unused_connection, err):
        logger.error("Connection open failed: %s", err)

    def on_connection_closed(self, _unused_connection, reason):
        logger.warning("Connection closed, reconnect necessary: %s", reason)
        self.channel.close()
        self.connection.close()


if __name__ == "__main__":
    try:
        Consumer().connect()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
