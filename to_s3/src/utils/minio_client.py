import os
import logging

from minio import Minio, ResponseError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:minio")


class MinioClient:
    
    
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        try:
            self.minio = Minio(endpoint=endpoint,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=secure)
        except KeyError as err:
            logger.error(err)
            raise Exception("Error! Please set appropriate values in config.ini")

    def fetch_file(self, bucket_name, object_name, file_path, version_id=None):
        try:
            return self.minio.fget_object(bucket_name=bucket_name, object_name=object_name,
                                  file_path=file_path, vesion_id=version_id)
        except Exception as err:
            logger.error(err)
            return None
