# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import logging
import os

import mysql.connector as db
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.misc import md5sum
from six import BytesIO

from .constants import base_unzip_path, zip_download_path
from .utils.file_service import FileService
from .utils.malicious_check import MaliciousCheck
from .utils.minio_client import MinioClient
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):

    def file_downloaded(self, response, request, info, unzip_path=None):

        try:
            self.conn = db.connect(
                host='localhost',
                user='root',
                password='12345678',
                database='gw',
            )
            self.cursor = self.conn.cursor()

        except Exception as err:
            raise err

        self.cursor = self.conn.cursor(buffered=True)
        query = "SELECT * from crawler_urls where url='%s' " % (response.url)

        self.cursor.execute(query)
        found = self.cursor.fetchall()

        if not found:

            path = self.file_path(request, response=response, info=info)
            buf = BytesIO(response.body)
            checksum = md5sum(buf)
            buf.seek(0)
            self.store.persist_file(path, buf, info)

            file_path = zip_download_path + "/" + path
            key = path.split("/")[-1].split(".")[0]

            FileService.unzip_files(file_path, key)
            unzip_path = base_unzip_path + "/" + key

            for file in os.listdir(unzip_path):
                file_path = unzip_path + "/" + file
                vt_report = MaliciousCheck.check_malicious(file_path)
                metadata = FileService.get_file_meta(path)
                zip_path = unzip_path + "/"
                with open(zip_path + 'metadata.txt', 'w') as outfile:
                    json.dump(metadata, outfile)
                with open(zip_path + 'vt_report.txt', 'w') as outfile:
                    json.dump(vt_report, outfile)
                zipped_file = FileService.zip_files(unzip_path, key=key)
                bucket_name = metadata["extension"]

                client = MinioClient.get_client()
                if not client.bucket_exists(bucket_name):
                    client.create_bucket(bucket_name)
                client.upload_file(bucket_name, path.split("/")[-1], zipped_file)

                self.cursor.execute("INSERT INTO crawler_urls (url, status) VALUES (%s, %s)", (response.url, True))
                self.conn.commit()
            return checksum


class MySQLPipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)

    def open_spider(self, spider):
        self.conn = db.connect(db=self.db,
                               user=self.user, passwd=self.passwd,
                               host=self.host,
                               charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.create_table()

        return item

    def close_spider(self, spider, reason):
        self.conn.close()

    def create_table(self):
        self.cursor.execute("""create table if not exists crawler_urls(url text,status boolean)""")


class UpdateStatsMiddleware(object):
    def __init__(self, crawler):
        self.crawler = crawler
        # register close_spider method as callback for the spider_closed signal
        crawler.signals.connect(self.close_spider, signals.spider_closed)

        try:
            self.conn = db.connect(
                host='localhost',
                user='root',
                password='12345678',
                database='gw',
            )
            self.cursor = self.conn.cursor()

        except Exception as err:
            raise err

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def get_jobid(self):
        """Gets jobid through scrapyd's SCRAPY_JOB env variable"""
        return os.environ['SCRAPY_JOB']

    def close_spider(self, spider, reason):

        # do your magic here...
        spider.log('Finishing spider with reason: %s' % reason)
        stats = self.crawler.stats.get_stats()
        jobid = self.get_jobid()
        self.update_job_stats(jobid, stats)

    def update_job_stats(self, jobid, stats):
        self.create_table()

        self.cursor.execute(
            "INSERT INTO crawler_job_details (job,item_scraped_count,finish_reason) VALUES (%s ,%s , %s)",
            (jobid, stats['item_scraped_count'], stats['finish_reason']))

        self.conn.commit()

        # do your magic here...

    def create_table(self):
        self.cursor.execute(
            """create table if not exists crawler_job_details(job text,item_scraped_count INT,finish_reason text)""")
