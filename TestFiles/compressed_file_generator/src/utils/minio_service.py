import logging

from minio import Minio

logger = logging.getLogger("GW:minio")


class MinioService:
    """
            It calls storage adapter to get minio client
    """

    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.minio_client = Minio(endpoint=url, access_key=access_key,
                                  secret_key=secret_key, secure=False)

    def upload(self, file_path, bucket_name, file_name):
        try:
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)
            logger.info("Uploading file to bucket {} minio {}".format(bucket_name, self.url))
            self.minio_client.fput_object(bucket_name=bucket_name, file_path=file_path, object_name=file_name)
        except Exception as e:
            logger.error(f'Minio_Service : upload : {e} ')

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

    def download_n_files(self, bucket_name, download_path, num_of_files):
        try:
            count = 0
            objects = self.minio_client.list_objects(bucket_name=bucket_name)
            for object in objects:
                path = download_path + "/" + object.object_name
                self.minio_client.fget_object(bucket_name=bucket_name, object_name=object.object_name, file_path=path)
                count = count + 1
                if count == num_of_files:
                    break
        except Exception as e:
            logger.error(e)
            raise e


    def list_buckets(self):
        try:
            list = []
            bucket_list = self.minio_client.list_buckets()
            for bucket in bucket_list:
                list.append(bucket.name)
            return list

        except Exception as e:
            logger.error(f'Minio_service: download_files : {e} ')




