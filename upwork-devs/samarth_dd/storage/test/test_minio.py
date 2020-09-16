from datetime import datetime
from unittest import TestCase
import pytz
from requests.cookies import MockResponse
from twisted.conch.test.test_channel import MockConnection
from minio.api import _DEFAULT_USER_AGENT
from minio.error import InvalidBucketError, NoSuchBucket
from storage.test.responses.minio_mocks import MockConnection ,MockResponse
from nose.tools import eq_, raises, timed
from unittest import mock
from storage.src.adapter_object_creator import ObjectCreator
from storage.src.minio_adapter import MinioAdapter


class TestMinioAdapter(TestCase):

    def setUp(self):
        self.adapter=ObjectCreator.get_storage_adapter(self)

    @raises(TypeError)
    def test_bucket_is_string(self):
        self.adapter.create_container(1234)

    @raises(InvalidBucketError)
    def test_bucket_is_not_empty_string(self):
        self.adapter.create_container('  \t \n  ')

    @raises(InvalidBucketError)
    def test_bucket_exists_invalid_name(self):
        self.adapter.create_container('AB*CD')


    @mock.patch('urllib3.PoolManager')
    def test_make_bucket_works(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('PUT',
                         'https://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200)
        )
        config={'HOSTNAME':'localhost:9000', "AWS_ACCESS_KEY_ID":None, 'AWS_SECRET_ACCESS_KEY':None}

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
        buckets = service.get_container_list()
        count = 0
        for bucket in buckets:
            count += 1
        eq_(0, count)

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
        buckets = service.get_container_list()
        buckets_list = []
        count = 0
        for bucket in buckets:
            count += 1
            buckets_list.append(bucket)
        eq_(2, count)
        eq_('hello', buckets_list[0].name)
        eq_(datetime(2015, 6, 22, 23, 7, 43, 240000,
                     pytz.utc), buckets_list[0].creation_date)
        eq_('world', buckets_list[1].name)
        eq_(datetime(2015, 6, 22, 23, 7, 56, 766000,
                     pytz.utc), buckets_list[1].creation_date)

    @raises(TypeError)
    def test_bucket_is_string(self):
        self.adapter.remove_container(1234)

    @raises(InvalidBucketError)
    def test_bucket_is_not_empty_string(self):
        self.adapter.remove_container('  \t \n  ')

    @raises(InvalidBucketError)
    def test_remove_bucket_invalid_name(self):
        self.adapter.remove_container('AB*CD')

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
                         {'User-Agent': _DEFAULT_USER_AGENT}, 200, content=mock_data)
        )
        mock_server.mock_add_request(
            MockResponse('DELETE',
                         'http://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT}, 204)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        service.remove_container('hello')

    @raises(InvalidBucketError)
    def test_object_is_string(self):
        self.adapter.remove_file('hello',1234)

    @raises(InvalidBucketError)
    def test_object_is_not_empty_string(self):
        self.adapter.remove_file('hello', '  \t \n  ')

    @mock.patch('urllib3.PoolManager')
    @raises(NoSuchBucket)
    def test_get_policy_for_non_existent_bucket(self, mock_connection):
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
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None,'SECURE':True}
        service = MinioAdapter(config)
        service.get_policy(bucket_name)

    @mock.patch('urllib3.PoolManager')
    def test_empty_list_objects_works(self, mock_connection):
        mock_data = '''<?xml version="1.0" encoding="UTF-8"?>
    <ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
      <Name>bucket</Name>
      <Prefix></Prefix>
      <KeyCount>0</KeyCount>
      <MaxKeys>1000</MaxKeys>
      <Delimiter></Delimiter>
      <IsTruncated>false</IsTruncated>
    </ListBucketResult>'''
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse(
                "GET",
                'http://localhost:9000/bucket/?delimiter=%2F'
                "&max-keys=1000&prefix=",
                {"User-Agent": _DEFAULT_USER_AGENT},
                200,
                content=mock_data,
            ),
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None,
                  'SECURE': False}
        client = MinioAdapter(config)
        object_iter = client.get_all_files('bucket')
        objects = []
        for obj in object_iter:

            objects.append(obj)
        print(len(objects))
        eq_(0, len(objects))

    def test_list_objects(self):
        @mock.patch('urllib3.PoolManager')
        def test_empty_list_objects_works(self, mock_connection):
            mock_data = '''<?xml version="1.0" encoding="UTF-8"?>
        <ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
          <Name>bucket</Name>
          <Prefix></Prefix>
          <KeyCount>0</KeyCount>
          <MaxKeys>1000</MaxKeys>
          <Delimiter></Delimiter>
          <IsTruncated>false</IsTruncated>
        </ListBucketResult>'''
            mock_server = MockConnection()
            mock_connection.return_value = mock_server
            mock_server.mock_add_request(
                MockResponse(
                    "GET",
                    "https://localhost:9000/bucket/?delimiter=&list-type=2"
                    "&max-keys=1000&prefix=",
                    {"User-Agent": _DEFAULT_USER_AGENT},
                    200,
                    content=mock_data,
                ),
            )
            config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None,
                      'SECURE': False}
            client = MinioAdapter(config)
            object_iter = client.get_all_files('bucket')
            objects = []
            for obj in object_iter:
                objects.append(obj)
            eq_(0, len(objects))

        @timed(1)
        @mock.patch('urllib3.PoolManager')
        def test_list_objects_works(self, mock_connection):
            mock_data = '''<?xml version="1.0" encoding="UTF-8"?>
        <ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
          <Name>bucket</Name>
          <Prefix></Prefix>
          <KeyCount>2</KeyCount>
          <MaxKeys>1000</MaxKeys>
          <IsTruncated>false</IsTruncated>
          <Contents>
            <Key>6/f/9/6f9898076bb08572403f95dbb86c5b9c85e1e1b3</Key>
            <LastModified>2016-11-27T07:55:53.000Z</LastModified>
            <ETag>&quot;5d5512301b6b6e247b8aec334b2cf7ea&quot;</ETag>
            <Size>493</Size>
            <StorageClass>REDUCED_REDUNDANCY</StorageClass>
          </Contents>
          <Contents>
            <Key>b/d/7/bd7f6410cced55228902d881c2954ebc826d7464</Key>
            <LastModified>2016-11-27T07:10:27.000Z</LastModified>
            <ETag>&quot;f00483d523ffc8b7f2883ae896769d85&quot;</ETag>
            <Size>493</Size>
            <StorageClass>REDUCED_REDUNDANCY</StorageClass>
          </Contents>
        </ListBucketResult>'''
            mock_server = MockConnection()
            mock_connection.return_value = mock_server
            mock_server.mock_add_request(
                MockResponse(
                    "GET",
                    "https://localhost:9000/bucket/?delimiter=%2F&list-type=2"
                    "&max-keys=1000&prefix=",
                    {"User-Agent": _DEFAULT_USER_AGENT},
                    200,
                    content=mock_data,
                ),
            )
            config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None,
                      'SECURE': False}
            client = MinioAdapter(config)
            objects_iter = client.get_all_files(client)
            count=client.count_files(client)
            objects = []
            for obj in objects_iter:
                objects.append(obj)

            eq_(2, count)

    @raises(InvalidBucketError)
    @mock.patch('minio.Minio.fput_object')
    def test_upload_file(self,mock_put):
        self.adapter.upload_file(mock.Mock(),mock.Mock(),mock.Mock())
        mock_put.assert_called_with('bucket','file','path')



