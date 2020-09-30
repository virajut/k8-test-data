# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy.loader import ItemLoader
from src.items import MaliciousFileCrawlerItem
from src.spiders.scraper import Scraper
from src.utils.read_config import ConfigReader

logger = logging.getLogger(__name__)
prefs = {'profile.default_content_setting_values.automatic_downloads': 1}


# remoteWebDriverUrl = "http://192.168.99.100:4444/wd/hub"

class GlasswallScraper(Scraper):
    name = 'glasswall'

    def __init__(self, config=None, data=None, **kwargs):

        super(GlasswallScraper, self).__init__()
        self.cfg = ConfigReader(config.upper()).read_config()
        self.login_url = self.cfg.get('login_url')
        self.start_urls = [self.login_url]
        self.file_page_url = self.cfg.get("file_page_url")

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """
        try:
            logging.info(f"start requests: {self.start_urls}")
            for url in self.start_urls:
                yield scrapy.Request(url,
                                     callback=self.navigate_to)
        except Exception as err:
            logger.error(f'GlasswallScraper:start_requests : {err}')
            raise err

    def navigate_to(self, response):
        try:
            yield scrapy.Request(self.file_page_url,
                                 callback=self.download_files)
        except Exception as err:
            logger.error(f'GlasswallScraper:navigate_to : {err}')
            raise err

    def download_files(self, response):
        try:
            download_all_link = response.xpath("//li[@id='download']/a/@href").get()
            loader = ItemLoader(item=MaliciousFileCrawlerItem())
            loader.add_value('file_urls', download_all_link)
            yield loader.load_item()

        except Exception as err:
            logger.error(f'GlasswallScraper:download_files : {err}')
            raise err
