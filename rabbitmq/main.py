import logging
import time

logger = logging.getLogger('GW: RabbitMQ Main')

from src.publisher import Publisher
from src.consumer import Consumer
from multiprocessing import Process

if __name__ == "__main__":
    time.sleep(30)
    try:
        publisher = Process(target=Publisher.run)
        publisher.start()
    except:
        pass
    try:
        consumer = Process(target=Consumer.run)
        consumer.start()
    except Exception as error:
        logger.error(f'main: error {error}')
