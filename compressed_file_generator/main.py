import logging as logger
import os
import shutil

from src.config import Config
from src.utils.compress import Compress
from src.utils.s3_client import S3Client
from src.utils.minio_service import MinioService

logger.basicConfig(level=logger.INFO)

class Process:
    def __init__(self):
        self.s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
        self.num_of_files = Config.NUM_OF_FILES

    def compress_and_upload(self, file_path, file_name):
        target = Config.upload_path
        try:
            logger.info(f'zipping file {file_path} to .zip compression')
            zip_name = Compress.zip_compresstion(target, file_name, file_path)
            bucket_name = 'zip'
            target_file_path = target + file_name + '.' + bucket_name
            logger.info(f'target_file_path {target_file_path}')
            self.s3_client.upload_file(file_path=target_file_path, file_name=zip_name, bucket=bucket_name)
        except Exception as err:
            logger.error(f'Process:compress_and_upload: .zip error {err}')
            raise Exception(f'Error while .zip compression and uploading {err}')

        try:
            logger.info(f'zipping file {file_path} to .7z compression')
            z_name = Compress.seven_z_compresstion(target, file_name, file_path)
            bucket_name = '7z'
            target_file_path = target + file_name + '.' + bucket_name
            self.s3_client.upload_file(file_path=target_file_path, file_name=z_name, bucket=bucket_name)
        except Exception as err:
            logger.error(f'Process:compress_and_upload: .7z error {err}')
            raise Exception(f'Error while .7z compression and uploading {err}')

        try:
            logger.info(f'zipping file {file_path} to .tar compression')
            tar_name = Compress.tar_compresstion(target, file_name, file_path)
            bucket_name = 'tar'
            target_file_path = target + file_name + '.' + bucket_name
            self.s3_client.upload_file(file_path=target_file_path, file_name=tar_name, bucket=bucket_name)
        except Exception as err:
            logger.error(f'Process:compress_and_upload: .tar error {err}')
            raise Exception(f'Error while .tar compression and uploading {err}')

        try:
            logger.info(f'zipping file {file_path} to .gz compression')
            gz_name = Compress.gz_compresstion(target, file_name, file_path)
            bucket_name = 'gz'
            try:
                name, ext = file_path.split("/")[-1].split(".")
            except:
                ext = 'txt'
            target_file_path = target + file_name + '.' + ext + "." + bucket_name
            self.s3_client.upload_file(file_path=target_file_path, file_name=gz_name, bucket=bucket_name)
        except Exception as err:
            logger.error(f'Process:compress_and_upload: .gz error {err}')
            raise Exception(f'Error while .gz compression and uploading {err}')

        try:
            logger.info(f'zipping file {file_path} to .rar compression')
            rar_name = Compress.rar_compresstion(target, file_name, file_path)
            bucket_name = 'rar'
            target_file_path = target + file_name + '.' + bucket_name
            self.s3_client.upload_file(file_path=target_file_path, file_name=rar_name, bucket=bucket_name)
        except Exception as err:
            logger.error(f'Process:compress_and_upload: .rar error {err}')
            raise Exception(f'Error while .rar compression and uploading {err}')


if __name__ == "__main__":

    try:
        if not os.path.exists(Config.download_path):
            os.makedirs(Config.download_path)
        else:
            shutil.rmtree(Config.download_path)
            os.makedirs(Config.download_path)
        if not os.path.exists(Config.upload_path):
            os.makedirs(Config.upload_path)
        else:
            shutil.rmtree(Config.upload_path)
            os.makedirs(Config.upload_path)

        process = Process()

        if os.environ.get('source_type','s3')=='minio':
            logger.info("Downloading malware files from minio")
            minio_client = MinioService(url=Config.MINIO_URL, access_key=Config.MINIO_ACCESS_KEY,
                                             secret_key=Config.MINIO_SECRET_KEY)
            minio_client.download_n_files(num_of_files=process.num_of_files)

        else:
            process.s3_client.download_files(Config.SOURCE_S3_BUCKET, process.num_of_files)

    except Exception as err:
        logger.error(f'Main : dwonlaod error : {err}')
        raise Exception(f'Main:Error while downloading files {err}')

    files = []
    _files = os.listdir(Config.download_path)

    if not _files:
        logger.error("file of required file type not present inside the bucket")
    else:
        try:
            for f in _files:
                if os.path.isfile(Config.download_path + f):
                    file_path = Config.download_path + f
                    file_name = f.split(".")[0]
                    process.compress_and_upload(file_path=file_path, file_name=file_name)
        except Exception as err:
            logger.error(f'main: compress_and_upload_err {err}')
            raise err

    try:
        shutil.rmtree(Config.download_path)
        shutil.rmtree(Config.upload_path)
    except Exception as err:
        logger.error((f'Error while deleted download upload path'))
        raise err
