import pika, sys, os
import requests
import logging as logger

logger.basicConfig(level=logger.INFO)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.environ["MQ_HOST"])
    )
    channel = connection.channel()

    channel.queue_declare(queue=os.environ["MQ_QUEUE"])  # , durable=True)

    def callback(ch, method, properties, body):
        logger.info(" [x] Received ")
        msg = body.decode()
        logger.info(msg)
        # to do
        if "process_zip" in msg:
            logger.info("calling file_processor service..")
            requests.post("http://k8-file-processor:5001/process", json={"msg": msg})
        elif "s3_sync" in msg:
            logger.info("calling s3_sync service..")
        # to do

        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=os.environ["MQ_QUEUE"], on_message_callback=callback)

    logger.info(" [*] starting receiver..")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
