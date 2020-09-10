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

    def download_files(self, bucket_name, num_files):

        try:
            file_path = "./"
            logger.debug("Check if the Bucket {} exists".format(bucket_name))
            if self.s3.Bucket(bucket_name) not in self.s3.buckets.all():
                raise Exception(f"{bucket_name} bucket does not exist")
            bucket = self.s3.Bucket(bucket_name)
            files_list = []
            saved_files = 0
            for files in bucket.objects.all():
                path, filename = os.path.split(files.key)
                obj_file = file_path + filename
                logger.debug("Downloading file {}.".format(filename))
                bucket.download_file(files.key, obj_file)
                files_list.append(obj_file)
                saved_files += 1
                if saved_files == num_files:
                    break
            return files_list
        except ClientError as e:
            logger.error(
                "Cannot Connect to the Minio {}. Please Verify your credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(e)

    def upload_to_minio(self, file_path, bucket_name, filename):

        try:
            logger.debug("Checking if the Bucket to upload files exists or not.")
            if (self.s3.Bucket(bucket_name) in self.s3.buckets.all()) == False:
                logger.info("Bucket not Found. Creating Bucket.")
                self.s3.create_bucket(Bucket=bucket_name)
            logger.debug(
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
        except e:
            logger.error(e)
