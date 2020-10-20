import ast
import logging as logger
import os
import shutil

import requests
from src.config import Config
from src.utils.compress import Compress
from src.utils.s3_client import S3Client

logger.basicConfig(level=logger.INFO)


class Process:
    def __init__(self):
        self.s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
        self.num_of_files = Config.NUM_OF_FILES
        self.target = Config.upload_path
        self.server_base_url = os.environ.get('server_base_url')
        self.not_allowed_types = ["zip", "7z", "rar", "tar", "gz"]

    def compress_file(self):
        try:
            target = self.target
            _files = os.listdir(Config.download_path)
            if not _files:
                logger.error("file of required file type not present inside the bucket")
            for f in _files:
                if os.path.isfile(Config.download_path + f):
                    file_path = Config.download_path + f
                    file_name = f.split(".")[0]
                    logger.info(f'zipping file {file_path}')

                    Compress.zip_compresstion(target, file_name, file_path)
                    Compress.seven_z_compresstion(target, file_name, file_path)
                    Compress.tar_compresstion(target, file_name, file_path)
                    Compress.gz_compresstion(target, file_name, file_path)
                    Compress.rar_compresstion(target, file_name, file_path)

        except Exception as err:
            logger.info(f"Process : compress : {err}")


    def upload_s3(self):
        try:
            _files = os.listdir(Config.upload_path)
            for file_name in _files:
                file = Config.upload_path + file_name
                print(file)
                folder_name = file_name.split(".")[-1]
                print('fddll')
                payload = {'bucket_name': os.environ["TARGET_S3_BUCKET"], 'folder_name': folder_name}
                files = {"file": (file_name, open(file, "rb")), }

                requests.post(self.server_base_url + "upload_to_s3", files=files, params=payload)
        except Exception as e:
            logger.info(f"Process : upload_to_s3 : {e}")
            raise e

    def download_n_files_from_s3(self, bucket_name, num_files):
        try:
            json = {'bucket_name': bucket_name, 'num_files': num_files}
            return requests.post(self.server_base_url + "s3_download", json=json)
        except Exception as e:
            logger.error(f'MinioClient : upload_stream : {e} ')

    def list_files_from_minio(self, bucket_name):
        try:
            json = {'bucket_name': bucket_name}
            return requests.post(self.server_base_url + "list_files", json=json)
        except Exception as e:
            logger.error(f'MinioClient : list_files_from_minio : {e} ')

    def list_buckets_from_minio(self):
        try:
            return requests.post(self.server_base_url + "list_buckets")
        except Exception as e:
            logger.error(f'MinioClient : upload_stream : {e} ')

    def download_file_from_minio(self, bucket, file_name):
        try:
            json = {'bucket_name': bucket, "object_name": file_name}
            response = requests.get(self.server_base_url + "download_from_minio/" + file_name, json=json)
            content = response.content.decode()
            f = open(Config.download_path + file_name, "w")
            f.write(content)
            f.close()
            return True
        except Exception as e:
            logger.error(f'MinioClient : download_file_from_minio : {e} ')
            return False

    def download_n_files_from_minio(self, num_of_files):
        count = 0
        bucket_list = self.list_buckets_from_minio()
        bucket_list = ast.literal_eval(bucket_list.content.decode())
        for bucket in bucket_list["list"]:
            files = self.list_files_from_minio(bucket_name=bucket)
            file_response = ast.literal_eval(files.content.decode())
            for f in file_response['list']:
                if count == num_of_files:
                    break
                else:
                    if not bucket in self.not_allowed_types:
                        status = self.download_file_from_minio(bucket=bucket, file_name=f)
                        if status:
                            print("true")
                            count = count + 1

if __name__ == "__main__":

    try:
        if not os.path.exists(Config.download_path):
            os.makedirs(Config.download_path)
        if not os.path.exists(Config.upload_path):
            os.makedirs(Config.upload_path)

        process = Process()
        logger.info("main : Downloading malware files from minio")
        process.download_n_files_from_minio(Config.NUM_OF_FILES)

    except Exception as err:
        logger.error(f'Main : dwonlaod error : {err}')
        raise Exception(f'Main:Error while downloading files {err}')

    try:
        process.compress_file()
        print("compressed")
        re = process.upload_s3()
        print(re)
    except Exception as err:
        logger.error(f'main: compress and upload file error : {err}')
        raise err

    try:
        shutil.rmtree(Config.download_path)
        shutil.rmtree(Config.upload_path)
    except Exception as err:
        logger.error((f'Error while deleted download upload path'))
        raise err
