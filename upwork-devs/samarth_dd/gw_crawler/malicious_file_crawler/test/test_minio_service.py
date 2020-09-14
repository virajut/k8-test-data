import os
from unittest import TestCase

from gw_crawler.malicious_file_crawler.src.utils.minio_service import MinioService


class TestMinioService(TestCase):

    def setUp(self):
        self.minioClient=MinioService(os.environ['HOSTNAME'],os.environ['AWS_ACCESS_KEY'],os.environ['AWS_SECRET_ACCESS_KEY'])

    def test_create_bucket(self):
        pass

    def test_delete_bucket(self):
        pass

    def test_list_buckets(self):
        pass

    def test_upload_files(self):
        pass

    def test_upload_stream(self):
        pass

    def test_download_bucket(self):
        pass

    def test_download_files(self):
        pass