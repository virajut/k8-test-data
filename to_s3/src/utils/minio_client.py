import os
import logging

from minio import Minio, ResponseError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:to_s3")


class MinioClient:
    
    def __init__(self):
        try:
            self.minio = Minio(endpoint=AppConfig.MINIO_ENDPOINT,
                               access_key=AppConfig.MINIO_ACCESS_KEY_ID,
                               secret_key=AppConfig.MINIO_SECRET_ACCESS_KEY,
                               secure=AppConfig.MINIO_SECURE)
            
            logger.info("Connected to Minio Server")
        except KeyError as err:
            logger.error(err)
            raise Exception("Error! Please set appropriate values .env file.")

    def fetch_file(self, bucket_name, object_name, file_path, version_id=None):
        try:
            return self.minio.fget_object(bucket_name=bucket_name, object_name=object_name,
                                  file_path=file_path, vesion_id=version_id)
        except Exception as err:
            logger.error(err)
            return Exception("Unable to fetch file from MinIO")
