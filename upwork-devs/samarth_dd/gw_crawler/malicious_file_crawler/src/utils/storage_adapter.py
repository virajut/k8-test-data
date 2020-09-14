import logging

from minio import ResponseError

logger = logging.getLogger()

class StorageAdapter(object):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """
    def __init__(self,*args, **kwargs):
        """
        Initialize common attributes shared by all storage adapters.
        """
        self.kwargs = kwargs
        self.logger = kwargs.get('logger', logging.getLogger(__name__))


    def create_bucket(self,bucket_name,region,object_lock):
        pass

    def delete_bucket(self,bucket_name):
        pass

    def get_all_buckets(self):
        pass

    def upload_file(self,bucket_name,file_name,file_path):
        pass

    def upload_data_stream(self,bucket_name,filename,data_stream,type):
        pass

    def download_bucket_files(self,bucket_name,path=None):
        pass

    def download_file(self,bucket_name,name,path):
        pass

    def set__policy(self,bucket_name):
        pass