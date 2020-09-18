import os
import logging
import boto3
import time
from botocore.client import Config
from botocore.exceptions import ClientError
from src.config import Config as AppConfig

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
            logger.info("Check if the Bucket {} exists".format(bucket_name))
            if self.s3.Bucket(bucket_name) not in self.s3.buckets.all():
                raise Exception(f"{bucket_name} bucket does not exist")
            bucket = self.s3.Bucket(bucket_name)
            files_list = []
            saved_files = 0
            for files in bucket.objects.all():
                try:
                    path, filename = os.path.split(files.key)
                    obj_file = file_path + filename
                    logger.info("Downloading file {}.".format(filename))
                    bucket.download_file(files.key, obj_file)
                    files_list.append(obj_file)
                    saved_files += 1
                    if saved_files == num_files:
                        break
                except Exception as ex:
                    print(ex)
                    continue
            return files_list
        except ClientError as e:
            logger.error(
                "Cannot Connect to the Minio {}. Please Verify your credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(e)
