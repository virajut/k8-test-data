# Import MinIO library.
import json

import minio
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import logging
from io import BytesIO

from gw_crawler.malicious_file_crawler.src.utils.storage_adapter import StorageAdapter

logger = logging.getLogger()

class MinioService(StorageAdapter):
    def __init__(self, hostname, access_key, secret_key, *args, **kwargs):
        # Initialize minioClient with an endpoint and access/secret keys.
        super().__init__(*args, **kwargs)
        self.minioClient =  Minio(hostname,
                                access_key=access_key,
                                secret_key=secret_key,
                                secure=True)

    def create_bucket(self,bucket_name,region,object_lock):
        # Make a bucket with the make_bucket API call.

        found = self.minioClient.bucket_exists(bucket_name)
        if found:
            raise Exception(f"{bucket_name} already exists exist")
        else:
            try:
                self.minioClient.make_bucket(bucket_name, location=region,object_lock=object_lock)
            except ResponseError as err:
                logger.error(err)
                raise ResponseError

    def delete_bucket(self,bucket_name):
        try:
            if (self.minioClient.bucket_exists(bucket_name)):
                self.minioClient.remove_bucket(bucket_name)
        except Exception as e:
            raise e

    def get_all_buckets(self):
        bucket_list = self.minioClient.list_buckets()
        return bucket_list


    def upload_file(self,bucket_name,file_name,file_path):
        if(not self.minioClient.bucket_exists(bucket_name)):
            self.minioClient.make_bucket(bucket_name=bucket_name)

        try:
            self.minioClient.fput_object(bucket_name=bucket_name,object_name=file_name,file_path=file_path)
            logger.info(f"Uploaded file {file_name}")
        except ResponseError as e:
            logger.error(e)
            raise Exception(e)

    def upload_data_stream(self,bucket_name,filename,data_stream,type):
        length = len(data_stream)
        try:
            if (self.minioClient.bucket_exists(bucket_name)):
                self.minioClient.put_object(bucket_name=bucket_name,object_name=filename,data=data_stream,length=length,content_type=type)
        except ResponseError as err:
            raise err


    def download_bucket_files(self,bucket_name,path=None):
        try:
            if (self.minioClient.bucket_exists(bucket_name)):
                bucket_list = self.minioClient.list_objects(bucket_name)
                for bucket in bucket_list:
                    self.minioClient.fget_object(bucket_name=bucket_name,object_name=bucket,file_path=path)
        except Exception as e:
            raise e

    def download_file(self,bucket_name,name,path):
        try:
            file=self.minioClient.fget_object(bucket_name=bucket_name,object_name=name,file_path=path)
        except ResponseError as e:
            raise e

        return file

    def set_readonly_policy(self,bucket_name):
        try:
            policy_read_only = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:GetBucketLocation",
                        "Resource": "arn:aws:s3:::" + bucket_name
                    },
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:ListBucket",
                        "Resource": "arn:aws:s3:::" + bucket_name
                    },
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:GetObject",
                        "Resource": "arn:aws:s3:::" + bucket_name
                    }
                ]
            }
            self.minioClient.set_bucket_policy(bucket_name,json.dumps(policy_read_only))
        except ResponseError as err:
            raise err


    def set_read_write_policy(self,bucket_name):
        try:
            policy_read_write = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": ["s3:GetBucketLocation"],
                        "Sid": "",
                        "Resource": ["arn:aws:s3:::"+bucket_name],
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"}
                    },
                    {
                        "Action": ["s3:ListBucket"],
                        "Sid": "",
                        "Resource": ["arn:aws:s3:::"+bucket_name],
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"}
                    },
                    {
                        "Action": ["s3:ListBucketMultipartUploads"],
                        "Sid": "",
                        "Resource": ["arn:aws:s3:::"+bucket_name],
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"}
                    },
                    {
                        "ction": ["s3:ListMultipartUploadParts",
                                   "s3:GetObject",
                                   "s3:AbortMultipartUpload",
                                   "s3:DeleteObject",
                                   "s3:PutObject"],
                        "Sid": "",
                        "Resource": ["arn:aws:s3:::"+bucket_name+"/*"],
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"}
                    }
                ]
            }

            self.minioClient.set_bucket_policy(bucket_name, json.dumps(policy_read_write))
        except ResponseError as err:
            raise err

    def set_write_policy(self, bucket_name):
        try:
            policy_write_only = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": "s3:GetBucketLocation",
                            "Resource": "arn:aws:s3:::"+bucket_name
                        },
                        {"Sid": "",
                         "Effect": "Allow",
                         "Principal": {"AWS": "*"},
                         "Action": "s3:ListBucketMultipartUploads",
                         "Resource": "arn:aws:s3:::"+bucket_name
                         },
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": [
                                "s3:ListMultipartUploadParts",
                                "s3:AbortMultipartUpload",
                                "s3:DeleteObject",
                                "s3:PutObject"],
                            "Resource":"arn:aws:s3:::"+bucket_name
                        }
                    ]
                }
            self.minioClient.set_bucket_policy(bucket_name, json.dumps(policy_write_only))
        except ResponseError as err:
            raise err







