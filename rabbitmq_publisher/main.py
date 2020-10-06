import os
import logging
import schedule
import time
from queue import Queue

from src.config import Config
from src.utils.minio_client import MinioClient
from src.utils.rabbit_client import RabbitClient

logger = logging.getLogger('GW: RabbitMQ Publisher')


def publish_jobs():
    logger.info('publish_jobs')

    minio_client = MinioClient()
    minio_files = []
    q = Queue()
    buckets = minio_client.get_all_buckets()
    if buckets:
        for bucket in buckets:
            logger.info(f'publish_jobs:bucket is {bucket}')
            minio_files = []
            minio_files = minio_client.get_all_files(bucket)
            for f in minio_files:
                logger.info(f'publish_jobs:File is {f}')
                payload = {"type": "process_zip", "file": f, "bucket": bucket}
                try:
                    q.put(payload)
                except Exception as err:
                    logger.error(err)
    RabbitClient(q)


if __name__ == "__main__":

    try:
        schedule.every(1).minutes.do(publish_jobs)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as err:
        logger.error(str(err))

    # Kept this code for demo purpose. On demo, it can be called without delay

    # try:
    #     publish_jobs()
    # except Exception as err:
    #     logging.error(str(err))



