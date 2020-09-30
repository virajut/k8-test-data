import os
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:minio")


class S3Client:

    def __init__(self, endpoint, access_key, secret_key, region=None):
        self.region = region
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
            region=region
        )


    """
        1. Check if bucket exists
        2. Check if file already exists
        3. Upload the file
    """
    
    def bucket_exists(self, bucket_name):
        if self.s3.meta.client.head_bucket(Bucket=bucket_name):
            return True
        return False

    def create_bucket(self, bucket_name):
        try:
            if self.region is None:
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration= {'LocationConstraint': self.region})
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file(self, file_name, bucket_name, object_name=None):
        if (not self.s3.bucket_exists(bucket_name)):
            self.s3.create_bucket(bucket_name=bucket_name)

        if object_name is None:
            object_name = file_name
        try:
            self.s3.upload_file(file_name, bucket_name, object_name)
            logger.info(f"Uploaded file: {0}".format(file_name))
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def get_policy(self, bucket_name):
        policy = self.s3.get_bucket_policy(bucket_name)
        return policy

    def set_policy(self, bucket_name, policy):
        self.s3.set_bucket_policy(bucket_name, policy)

