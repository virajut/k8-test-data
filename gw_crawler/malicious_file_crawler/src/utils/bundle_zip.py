import json
import logging
import os

from src.constants import base_unzip_path, zip_download_path

from .file_service import FileService
from .malicious_check import MaliciousCheck
from .minio_client import MinioClient

logger = logging.getLogger(__name__)


class BundleZip:
    @staticmethod
    def process_malware(path, spider_name):
        """
                Fetch the file
                :Unzip the file
                :Get metadata of the file
                :Get virus total report
                :Bundle zip metadata,virus total report and malware file
                :Store it in minio
        """
        try:
            key = path.split("/")[-1].split(".")[0]
            unzip_path = base_unzip_path + "/" + key
            downloaded_file_path = zip_download_path + "/" + path
            bucket_name = spider_name

            ext = path.split("/")[-1].split(".")[-1]
            if 'zip' == ext:

                FileService.unzip_files(downloaded_file_path, key)
                for file in os.listdir(unzip_path):
                    file_path = unzip_path + "/" + file
                    zip_path = unzip_path + "/"

                    vt_report = MaliciousCheck.check_malicious(file_path)
                    metadata = FileService.get_file_meta(file_path)
                    minio_path = metadata['extension'] + "/" + path.split("/")[-1]

                    BundleZip.write_to_file(zip_path, 'metadata.txt', metadata)
                    BundleZip.write_to_file(zip_path, 'virus_total_report.txt', vt_report)

                    bundle_zip = FileService.zip_files(unzip_path, key=key)
                    BundleZip.store(bucket_name, minio_path, bundle_zip)
            else:
                metadata = FileService.get_file_meta(downloaded_file_path)
                minio_path = metadata['extension'] + "/" + path.split("/")[-1]
                BundleZip.store(bucket_name, minio_path, downloaded_file_path)


        except Exception as e:
            logger.error(f'BundleZip:process_malware:Error while processing file {e}')
            raise e

    @staticmethod
    def write_to_file(path, name, content):
        """
                write data to a file
        """
        try:
            with open(path + name, 'w') as outfile:
                json.dump(content, outfile)
        except Exception as e:
            logger.error(f'BundleZip:write_to_file:Error while processing file {e}')
            raise e

    @staticmethod
    def store(bucket_name, minio_path, bundle_zip):
        """
            Create bucket
            Store object in minio
        """
        try:
            client = MinioClient.get_client()
            if not client.bucket_exists(bucket_name):
                client.create_bucket(bucket_name)

            if not client.bucket_exists(bucket_name):
                client.create_bucket(bucket_name)
            client.upload_file(bucket_name, minio_path, bundle_zip)
        except Exception as e:
            logger.error(f'BundleZip:store:Error while processing file {e}')
            raise e
