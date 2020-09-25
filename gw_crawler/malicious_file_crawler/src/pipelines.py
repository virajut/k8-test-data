# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import logging
import os

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.misc import md5sum
from six import BytesIO
from src.constants import zip_download_path

from .utils.minio_client import MinioClient

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):

    def file_downloaded(self, response, request, info, unzip_path=None):
        """
            Downloads file
            Check metadat of file and gets extension
            Store it in minio with spidername as bucketname
        """
        logger.info(f'MaliciousFileCrawlerPipeline:file_downloaded:: Spider Name {info.spider.name}')
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        try:
            logger.info(f'MaliciousFileCrawlerPipeline:file_downloaded:: Response status {response.status}')
            if (response.status == 200):
                if (info.spider.name == "virusshare"):
                    file_name = response.headers["Content-Disposition"].split(b'filename=')[1].decode("utf-8")
                    path = FilesPipeline.MEDIA_NAME + "/" + file_name
                checksum = md5sum(buf)
                buf.seek(0)
                self.store.persist_file(path, buf, info)
                downloaded_file_path = zip_download_path + "/" + path
                bucket_name = "zip"
                minio_path = path.split("/")[-1]
                MaliciousFileCrawlerPipeline.store(bucket_name, minio_path, downloaded_file_path)

                return checksum

        except Exception as err:
            logger.error(f'MaliciousFileCrawlerPipeline:file_downloaded: {err}')
            raise err

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
