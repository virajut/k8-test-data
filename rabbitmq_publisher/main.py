import os
from concurrent import futures
import asyncio
import logging

from src.config import Config
from src.utils.minio_client import MinioClient
from src.utils.rabbit_client import RabbitClient

logger = logging.getLogger('GW: RabbitMQ Publisher')

loop = asyncio.get_event_loop()
rabbit_client = RabbitClient()

async def task(payload):
    """
        Put a job in RabbitMQ
            - Job will require payload to be published
            - Once done, Close the connection
    """
    try:
        logger.info("Publishing task in the remote Queue")
        await rabbit_client.publish_message(message=payload)
    except Exception as err:
        logger.error("Something went wrong in Asyncio coro")
        logger.error(err)


def publish_jobs():

    minio_client = MinioClient()
    minio_files = minio_client.get_all_files(Config.MINIO_BUCKET)

    futures = []
    for f in minio_files:
        payload = {'type': 'process_zip', 'file': f, 'bucket': 'zip'}
        futures.append(loop.create_task(task(payload)))
    await asyncio.gather(*futures)

    rabbit_client.close_connection()


if __name__ == "__main__":
    
    publish_jobs()


