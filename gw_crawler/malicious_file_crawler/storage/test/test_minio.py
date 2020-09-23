import os
import sys
from datetime import datetime
from datetime import datetime
from unittest import TestCase, mock

import pytz

from minio.api import _DEFAULT_USER_AGENT
from minio.error import InvalidBucketError, NoSuchBucket

from requests.cookies import MockResponse

from twisted.conch.test.test_channel import MockConnection

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from storage.src.minio_service import MinioService
from storage.src.minio_adapter import MinioAdapter
from storage.test.responses.minio_mocks import MockConnection, MockResponse
import pytest

class TestMinioAdapter(TestCase):

    def setUp(self):
        self.adapter = MinioService.get_storage_adapter()


    def test_bucket_is_string(self):
        with pytest.raises(TypeError):
            self.adapter.create_bucket(1234)

    def test_bucket_is_not_empty_string(self):
        with pytest.raises(InvalidBucketError):
            self.adapter.create_bucket('  \t \n  ')


    def test_bucket_exists_invalid_name(self):
        with pytest.raises(InvalidBucketError):
            self.adapter.create_bucket('AB*CD')

    @mock.patch('urllib3.PoolManager')
    def test_bucket_exists_works(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('HEAD',
                         'http://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        client = MinioAdapter(config)
        result = client.bucket_exists('hello')
        self.assertEquals(True, result)
        mock_server.mock_add_request(
            MockResponse('HEAD',
                         'http://localhost:9000/goodbye/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         404)
        )
        false_result = client.bucket_exists('goodbye')
        self.assertEquals(False, false_result)

    @mock.patch('urllib3.PoolManager')
    def test_make_bucket_works(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('PUT',
                         'http://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}

        service = MinioAdapter(config)

    @mock.patch('urllib3.PoolManager')
    def test_empty_list_buckets_works(self, mock_connection):
        mock_data = ('<ListAllMyBucketsResult '
                     'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                     '<Buckets></Buckets><Owner><ID>minio</ID><DisplayName>'
                     'minio</DisplayName></Owner></ListAllMyBucketsResult>')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('GET', 'http://localhost:9000/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200, content=mock_data)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        buckets = service.get_bucket_list()
        count = 0
        for bucket in buckets:
            count += 1
        self.assertEquals(0, count)

    @mock.patch('urllib3.PoolManager')
    def test_list_buckets_works(self, mock_connection):
        mock_data = ('<ListAllMyBucketsResult '
                     'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                     '<Buckets><Bucket><Name>hello</Name>'
                     '<CreationDate>2015-06-22T23:07:43.240Z</CreationDate>'
                     '</Bucket><Bucket><Name>world</Name>'
                     '<CreationDate>2015-06-22T23:07:56.766Z</CreationDate>'
                     '</Bucket></Buckets><Owner><ID>minio</ID>'
                     '<DisplayName>minio</DisplayName></Owner>'
                     '</ListAllMyBucketsResult>')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('GET', 'http://localhost:9000/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200, content=mock_data)
        )

        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        buckets = service.get_bucket_list()
        buckets_list = []
        count = 0
        for bucket in buckets:
            count += 1
            buckets_list.append(bucket)
        self.assertEquals(2, count)
        self.assertEquals('hello', buckets_list[0].name)
        self.assertEquals(datetime(2015, 6, 22, 23, 7, 43, 240000,
                     pytz.utc), buckets_list[0].creation_date)
        self.assertEquals('world', buckets_list[1].name)
        self.assertEquals(datetime(2015, 6, 22, 23, 7, 56, 766000,
                     pytz.utc), buckets_list[1].creation_date)

    def test_bucket_is_string(self):
        with pytest.raises(TypeError):
            self.adapter.remove_bucket(1234)

    def test_bucket_is_not_empty_string(self):
        with pytest.raises(InvalidBucketError):
            self.adapter.remove_bucket('  \t \n  ')

    def test_remove_bucket_invalid_name(self):
        with pytest.raises(InvalidBucketError):
            self.adapter.remove_bucket('AB*CD')

    def test_object_is_string(self):
        with pytest.raises(InvalidBucketError):
            self.adapter.remove_file('hello', 1234)

    def test_object_is_not_empty_string(self):
        with pytest.raises(InvalidBucketError):
            self.adapter.remove_file('hello', '  \t \n  ')

    @mock.patch('urllib3.PoolManager')
    def test_get_policy_for_non_existent_bucket(self, mock_connection):
        with pytest.raises(NoSuchBucket):
            mock_server = MockConnection()
            mock_connection.return_value = mock_server
            bucket_name = 'non-existent-bucket'
            mock_server.mock_add_request(
                MockResponse(
                    'GET',
                    'http://localhost:9000/' + bucket_name + '/?policy=',
                    {'User-Agent': _DEFAULT_USER_AGENT},
                    404,
                )
            )
            config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None,
                      'SECURE': True}
            service = MinioAdapter(config)
            service.get_policy(bucket_name)

    @mock.patch('urllib3.PoolManager')
    def test_remove_bucket_works(self, mock_connection):

        mock_data = ('<ListAllMyBucketsResult '
                     'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                     '<Buckets><Bucket><Name>hello</Name>'
                     '<CreationDate>2015-06-22T23:07:43.240Z</CreationDate>'
                     '</Bucket><Bucket><Name>world</Name>'
                     '<CreationDate>2015-06-22T23:07:56.766Z</CreationDate>'
                     '</Bucket></Buckets><Owner><ID>minio</ID>'
                     '<DisplayName>minio</DisplayName></Owner>'
                     '</ListAllMyBucketsResult>')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('HEAD',
                         'http://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200)
        )
        mock_server.mock_add_request(
            MockResponse('DELETE',
                         'http://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT}, 204)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        service.remove_bucket('hello')

