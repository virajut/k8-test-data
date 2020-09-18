import os
import logging
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger("GW:minio")


class Minio:
    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    def upload(self, file_path, bucket_name, filename):
        try:
            logger.info("Checking if the Bucket to upload files exists or not.")
            if (self.s3.Bucket(bucket_name) in self.s3.buckets.all()) == False:
                logger.info("Bucket not Found. Creating Bucket.")
                self.s3.create_bucket(Bucket=bucket_name)
            logger.info(
                "Uploading file to bucket {} minio {}".format(bucket_name, self.url)
            )
            self.s3.Bucket(bucket_name).upload_file(file_path, filename)
            return bucket_name + "/" + filename
        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error("ex : {}".format(e))
