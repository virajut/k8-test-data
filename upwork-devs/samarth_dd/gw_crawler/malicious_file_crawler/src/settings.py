# Scrapy settings for malicious_file_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

BOT_NAME = 'src'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

# Config file path
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.ini')

ROBOTSTXT_OBEY = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'src.middlewares.MaliciousFileCrawlerDownloaderMiddleware': 543,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "scrapy.pipelines.files.FilesPipeline": 1
}

DOWNLOAD_TIMEOUT = 12000

FILES_STORE = os.getenv("STORAGE_PATH")

# Uncomment this when MINIO service is running
# AWS_ENDPOINT_URL = 'http://minio.example.com:9000'
# AWS_ENDPOINT_URL = 'http://127.0.0.1:9000'
# AWS_USE_SSL = False
# AWS_VERIFY = False
# FILES_STORE =/minio/mybucket
# AWS_ACCESS_KEY_ID = 'key'
# AWS_SECRET_ACCESS_KEY= 'secret'

# max download size of 5gb
DOWNLOAD_MAXSIZE = os.getenv('MAX_SIZE')
