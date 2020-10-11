import logging
import time
from queue import Queue

import schedule
from src.utils.minio_client import MinioClient
from src.utils.rabbit_client import RabbitClient

logger = logging.getLogger('GW: RabbitMQ Publisher')


class Publisher:
    @staticmethod
    def publish_jobs():
        logger.info('publish_jobs')

        minio_client = MinioClient()
        minio_files = []
        q = Queue()
        buckets = minio_client.get_all_buckets()
        if buckets:
            for bucket in buckets:
                if not bucket == "processed":
                    logger.info(f'publish_jobs:bucket is {bucket}')
                    minio_files = []
                    minio_files = minio_client.get_all_files(bucket)
                    n = len(minio_files)
                    if n:
                        for f in minio_files:
                            logger.info(f'publish_jobs:File is {f}')
                            payload = {"type": "process_zip", "file": f, "bucket": bucket}
                            try:
                                q.put(payload)
                            except Exception as err:
                                logger.error(err)

        RabbitClient(q)

    @staticmethod
    def run():
        try:
            schedule.every(1).minutes.do(Publisher.publish_jobs)
            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as err:
            logger.error(str(err))
