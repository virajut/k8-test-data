import os
import sched
import time

from src.config import Config
from src.utils.minio_client import MinioClient
from src.utils.rabbit_client import RabbitClient


def publish_jobs():

    minio_client = MinioClient()
    minio_files = minio_client.get_all_files(Config.MINIO_BUCKET)

    """
        Create json object to put into the RabbitMQ job
        Message format should be followed
        Create RabbitMQ client
        Publish in RabbitMQ 
    """