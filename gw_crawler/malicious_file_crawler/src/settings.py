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
from src.constants import zip_download_path
from dotenv import load_dotenv

env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

PROJECT_NAME = 'malicious_file_crawler'
# Define JOBDIR path for pausing and resuming crawls
JOBDIR = 'crawls/spiders'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
FILES_STORE = zip_download_path

# Uncomment this when MINIO service is running
# max download size of 5gb
DOWNLOAD_MAXSIZE = 5368709120
