import os
from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock
from itemloaders import ItemLoader
from gw_crawler.malicious_file_crawler.src.spiders.glasswall_crawler import GlasswallScraper
from malicious_file_crawler.src.utils.read_config import ConfigReader
from malicious_file_crawler.src.items import MaliciousFileCrawlerItem


class TestGlasswallCrawler(TestCase):
    def setUp(self):
        site = 'corvus'
        config = ConfigReader(site.upper()).read_config()
        self.cfg = config
        self.scrapper = GlasswallScraper(self.cfg)

    def test_start_requests(self):
        self.url = os.getenv('login_url')
        content = self.scrapper.start_requests()
        self.assertIsNotNone(content)

    def test_download_files(self):
        content = self.scrapper.download_files(os.getenv('login_url'))
        self.assertIsNotNone(content)

    def test_navigate_to(self):
        url = 'https://cloud.corvusforensics.com/s/HDcCHLnQTGBnYBN'
        content = self.scrapper.navigate_to(Mock())
        self.assertIsNotNone(())
