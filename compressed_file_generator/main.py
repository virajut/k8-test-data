import logging as logger
import os
import shutil

from src.config import Config
from src.utils.compress import Compress
from src.utils.minio_service import MinioService
from src.utils.s3_client import S3Client

logger.basicConfig(level=logger.INFO)


class Process:
    def __init__(self):
        self.s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
        self.num_of_files = Config.NUM_OF_FILES
        self.target = Config.upload_path

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

    def upload_to_s3(self):
        try:
            _files = os.listdir(Config.upload_path)
            for f in _files:
                logger.info(f'uploading file {f}')
                bucket_name = f.split(".")[-1]
                zip_name = f
                target_file_path = Config.upload_path + f
                self.s3_client.upload_file(file_path=target_file_path, file_name=zip_name, bucket=bucket_name)
        except Exception as e:
            logger.info(f"Process : upload_to_s3 : {err}")
            raise e


if __name__ == "__main__":

    try:
        if not os.path.exists(Config.download_path):
            os.makedirs(Config.download_path)
        if not os.path.exists(Config.upload_path):
            os.makedirs(Config.upload_path)

        process = Process()

        if os.environ.get('source_type', 's3') == 'minio':
            logger.info("main : Downloading malware files from minio")
            minio_client = MinioService(url=Config.MINIO_URL, access_key=Config.MINIO_ACCESS_KEY,
                                        secret_key=Config.MINIO_SECRET_KEY)
            minio_client.download_n_files(num_of_files=process.num_of_files)

        else:
            process.s3_client.download_files(Config.SOURCE_S3_BUCKET, process.num_of_files)

    except Exception as err:
        logger.error(f'Main : dwonlaod error : {err}')
        raise Exception(f'Main:Error while downloading files {err}')

    try:
        process.compress_file()
        process.upload_to_s3()
    except Exception as err:
        logger.error(f'main: compress and upload file error : {err}')
        raise err

    try:
        shutil.rmtree(Config.download_path)
        shutil.rmtree(Config.upload_path)
    except Exception as err:
        logger.error((f'Error while deleted download upload path'))
        raise err
