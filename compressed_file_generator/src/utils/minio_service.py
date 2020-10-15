import logging

from minio import Minio
from src.config import Config
logger = logging.getLogger("GW:minio")


class MinioService:
    """
            It calls storage adapter to get minio client
    """

    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.minio_client = Minio(endpoint=url, access_key=access_key,
                                  secret_key=secret_key, secure=False)

    def download_files(self, bucket_name, file_name, download_path):
        try:
            path = download_path + "/" + file_name
            self.minio_client.fget_object(bucket_name=bucket_name, object_name=file_name, file_path=path)

        except Exception as e:
            logger.error(f'Minio_service: download_files : {e} ')

    def download_all_files(self, bucket_name, download_path):
        try:
            objects=self.minio_client.list_objects(bucket_name=bucket_name)
            for object in objects:
                path = download_path + "/" + object.object_name
                self.minio_client.fget_object(bucket_name=bucket_name, object_name=object.object_name, file_path=path)
        except Exception as e:
            logger.error(f'Minio_service: download_files : {e} ')


    def list_buckets(self):
        try:
            list = []
            bucket_list = self.minio_client.list_buckets()
            for bucket in bucket_list:
                list.append(bucket.name)
            return list

        except Exception as e:
            logger.error(f'Minio_service: download_files : {e}')

    def list_objects(self,bucket_name):
        try:
            list = []
            objects = self.minio_client.list_objects(bucket_name=bucket_name)
            for object in objects:
                list.append(object.object_name)
            return list

        except Exception as e:
            logger.error(f'Minio_service: download_files : {e}')

    def download_n_files(self, num_of_files):
        try:
            count = 0
            bucket_list = self.list_buckets()
            for bucket in bucket_list:
                logger.info(f'bucker_name : {bucket} ')
                objects = self.list_objects(bucket)
                for object in objects:
                    count = count + 1
                    if not object.split(".")[-1] in "zip":
                        logger.info(f'object name : {object} ')
                        self.download_files(bucket_name=bucket, file_name=object,
                                                         download_path=Config.download_path)
                    if count == num_of_files:
                        return count

            if count < num_of_files:
                logger.info("Not enough files in minio")

        except Exception as err:
            logger.error(f'Process:download_n_files: error {err}')
            raise err
        else:
            return None




