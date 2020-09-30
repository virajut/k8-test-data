# Scrapy settings for malicious_file_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

from src.constants import DOWNLOAD_PATH
from datetime import datetime
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
from dotenv import load_dotenv

env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

PROJECT_NAME = 'malicious_file_crawler'
# Define JOBDIR path for pausing and resuming crawls
#JOB_DIR = 'crawlers/spider-1'
# scrapyd endpoint
# SCRAPYD_ENDPOINT = 'http://localhost:6800'




# DOWNLOADER_MIDDLEWARES = {
#         'history.middleware.HistoryMiddleware': 901 # Right after HttpCacheMiddleware
# }

#EPOCH = True
# HISTORY = {
#     'STORE_IF'   : 'history.logic.StoreAlways',
#     'RETRIEVE_IF': 'history.logic.RetrieveAlways',
#     'BACKEND'    : 'history.storage.S3CacheStorage',
#     'S3_ACCESS_KEY': 'AKIAIULADVGM55FLEA7A',
#     'S3_SECRET_KEY': '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',
#     'S3_BUCKET'    : 'abcd',
#     'USE_PROXY'  : True,
# }

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
date = datetime.strftime(datetime.now(), '%Y%m%d')
HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 7
HTTPCACHE_DIR = 'httpcache'
#S3CACHE_URI='s3://AKIAIULADVGM55FLEA7A:lB2RehGmcyKaSLBLrEa7IWd6KF0Pxr5F9rYrvkCf@bucket/name'

EXTENSIONS = {
   'scrapy_dotpersistence.DotScrapyPersistence': 0,
}

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the path to the directory this file is in
CURR_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'src'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

# Config file path
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.ini')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'malicious_file_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
REACTOR_THREADPOOL_MAXSIZE = 20

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'src.middlewares.MaliciousFileCrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "src.pipelines.MaliciousFileCrawlerPipeline": 1,
    'src.middlewares.MaliciousFileCrawlerDownloaderMiddleware': 543,

}
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "src.pipelines.MaliciousFileCrawlerPipeline": 300,
}

DOWNLOAD_TIMEOUT = 12000

MEDIA_ALLOW_REDIRECTS = True
FILES_STORE = DOWNLOAD_PATH

# Uncomment this when MINIO service is running
# max download size of 5gb
DOWNLOAD_MAXSIZE = 5368709120
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False
