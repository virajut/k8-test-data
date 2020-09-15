from minio import Minio, ResponseError

from storage.src.storage_adapter import BaseStorageAdapter


class MinioAdapter(BaseStorageAdapter):
    def __init__(self, config, *args, **kwargs):
        # Initialize minioClient with an endpoint and access/secret keys.

        super().__init__(*args, **kwargs)
        self._client =  Minio(endpoint=config.get('HOSTNAME'),
                                access_key=config.get('AWS_ACCESS_KEY_ID'),
                                secret_key=config.get('AWS_SECRET_ACCESS_KEY'),
                                secure=False)

    def create_container(self,container_name):
        if self._client.bucket_exists(container_name):
            raise Exception(f"{container_name} already exists")
        else:
            try:
                self._client.make_bucket(container_name)
            except ResponseError as err:
                raise ResponseError

    def remove_container(self,container_name):
        try:
            if self._client.bucket_exists(container_name):
                self._client.remove_bucket(container_name)
        except Exception as e:
            raise e

    def remove_file(self,container_name,file_name):
        try:
            if self._client.bucket_exists(self._client):
                if(self._client.get_object(self._client,file_name)):
                    self._client.remove_object(container_name,file_name)
        except Exception as e:
            raise e

    def get_container_list(self):
        bucket_list = self._client.list_buckets()
        return bucket_list

    def get_all_files(self,container_name):
        pass

    def upload_file(self, container_name, file_name, file_path):
        if (not self._client.bucket_exists(container_name)):
            self._client.make_bucket(bucket_name=container_name)
        try:
            self._client.fput_object(bucket_name=container_name, object_name=file_name, file_path=file_path)
            self.logger.info(f"Uploaded file {file_name}")
        except ResponseError as e:
            self.logger.error(e)
            raise Exception(e)

    def upload_data_stream(self, container_name, file_name, data_stream, data_type):
        length = len(data_stream)
        if (not self._client.bucket_exists(container_name)):
            self._client.make_bucket(bucket_name=container_name)
        try:
            self._client.put_object(bucket_name=container_name, object_name=file_name, data=data_stream, length=length,
                                        content_type=type)
        except ResponseError as err:
            raise err

    def download_all_files(self, container_name, download_path):
        try:
            if (self._client.bucket_exists(container_name)):
                obj_list = self._client.list_objects(container_name)
                for obj in obj_list:
                    self._client.fget_object(bucket_name=container_name, object_name=obj, file_path=download_path)
        except Exception as e:
            raise e

    def download_n_files(self, container_name, download_path, num_of_files):
        try:
            count=0
            for file in self._client.list_objects(container_name):
                self._client.fget_object(bucket_name=container_name, object_name=file, file_path=download_path)
                count=count+1
                if count==num_of_files:
                    break
        except ResponseError as e:
            raise e

    def count_files(self, container_name):
        list=self._client.list_objects(container_name)
        return len(list)

    def get_policy(self, container_name):
        policy=self._client.get_bucket_policy(container_name)
        return policy

    def set_policy(self, container_name, policy):
        self._client.set_bucket_policy(container_name,policy)

