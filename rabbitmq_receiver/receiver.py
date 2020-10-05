import pika, sys, os, json
import requests
import logging as logger
import time
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
        requests.post("http://k8-file-processor:5000/process", json=payload)

    def _handler_s3_sync(self, payload):
        logger.info("calling s3_sync service..")
        requests.post("http://k8-s3-sync:5004/tos3", json=payload)

    def on_message_receive(self,ch, method, properties, body):
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
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ["MQ_HOST"])
        )
        channel = connection.channel()

        channel.queue_declare(queue=os.environ["MQ_QUEUE"])

        def callback(ch, method, properties, body):
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


        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=os.environ["MQ_QUEUE"], on_message_callback=self.on_message_receive)

        logger.info(" [*] starting receiver..")
        channel.start_consuming()


if __name__ == "__main__":
    time.sleep(15)
    try:
        Consumer().connect()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)