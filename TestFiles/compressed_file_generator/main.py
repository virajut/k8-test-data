import os
import  logging as logger
from src.config import Config
from src.utils.s3_client import S3Client
from src.utils import minio_service
from src.utils.compress import Compress


logger.basicConfig(level=logger.INFO)

class Process:
    def __init__(self):
        url = Config.S3_URL
        access_key = Config.S3_ACCESS_KEY
        secret_key = Config.S3_SECRET_KEY
        #self.s3_client = s3_client.S3Client(url, access_key, secret_key)
        self.minio_client = minio_service.MinioService(url=Config.MINIO_URL, access_key=Config.MINIO_ACCESS_KEY,
                                  secret_key=Config.MINIO_SECRET_KEY)

    def download_files(self):
        list=self.minio_client.list_buckets()
        for item in list:
            if not item=='zip' :
                self.minio_client.download_all_files(bucket_name=item,download_path=Config.download_path)

    def download_n_files(self,num_of_files):
        list=self.minio_client.list_buckets()
        for item in list:
            if not item=='zip' and not item=='processed':
                logger.info(f'bucker_name : {item} ')
                self.minio_client.download_n_files(bucket_name=item,download_path=Config.download_path,num_of_files=num_of_files)

if __name__ == "__main__":
    p=Process()
    p.download_n_files(2)
    target = Config.upload_path
    if not os.path.exists(Config.upload_path):
        os.makedirs(Config.upload_path)
    s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)

    files=[]
    _files = os.listdir(Config.download_path)
    if not _files:
        logger.error("no file inside zip")
    else:
        try:
            for f in _files:

                file_path=Config.download_path + f
                logger.info(f'file_path: {file_path}')
                file_name = f.split(".")[0]

                zip_name = Compress.zip_compresstion(target, file_name, file_path)
                bucket_name='zip'
                target_file_path = target + file_name + '.' + bucket_name
                logger.info(f'target_file_path {target_file_path}')
                s3_client.upload_file(file_path=target_file_path, file_name=zip_name, bucket=bucket_name)

                z_name = Compress.seven_z_compresstion(target, file_name, file_path)
                bucket_name = '7z'
                target_file_path=target + file_name + '.' + bucket_name
                logger.info(f'target_file_path {target_file_path}')
                s3_client.upload_file(file_path=target_file_path, file_name=z_name, bucket=bucket_name)

                tar_name = Compress.tar_compresstion(target, file_name, file_path)
                bucket_name = 'tar'
                target_file_path = target + file_name + '.' +bucket_name
                logger.info(f'target_file_path {target_file_path}')
                s3_client.upload_file(file_path=target_file_path, file_name=tar_name, bucket=bucket_name)

                gz_name = Compress.gz_compresstion(target, file_name, file_path)
                bucket_name = 'tar'
                target_file_path = target + file_name + '.' + bucket_name
                logger.info(f'target_file_path {target_file_path}')
                s3_client.upload_file(file_path=target_file_path, file_name=gz_name, bucket=bucket_name)

        except Exception as err:
            logger.error(f'create_app: s3_client {err}')
            raise err

# if __name__ == "__main__":
#     src='/Users/samarthbharadwaj/Desktop/demo/k8-test-data/Test files/compressed_file_generator/repo/0d4f4608ecf4e2f381a3df763dfc39a3fba4b18c.xml'
#
#     target = Config.upload_path
#     name = src.split("/")[-1].split(".")[0]
#
#     Compress.rar_compresstion(target, name, src)






