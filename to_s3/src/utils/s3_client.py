import os
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:to_s3")


class S3Client:

    def __init__(self):
        self.region = AppConfig.S3_REGION

        try:
            self.s3 = boto3.resource(
                "s3",
                endpoint_url=AppConfig.S3_ENDPOINT,
                aws_access_key_id=AppConfig.S3_ACCESS_KEY_ID,
                aws_secret_access_key=AppConfig.S3_SECRET_ACCESS_KEY,
                config=Config(signature_version="s3v4"),
                region=AppConfig.S3_REGION
            )
            logger.info("Connected to S3 endpoint")
        except Exception as err:
            logger.error(err)
            raise Exception("Unable to connect to S3 endpoint")

    
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
            logger.info(f"File uploaded to S3: {0}".format(file_name))
            return True
        except ClientError as e:
            logging.error(e)
            raise Exception("Unable to upload the file to S3 server.")

    def get_policy(self, bucket_name):
        policy = self.s3.get_bucket_policy(bucket_name)
        return policy

    def set_policy(self, bucket_name, policy):
        self.s3.set_bucket_policy(bucket_name, policy)

