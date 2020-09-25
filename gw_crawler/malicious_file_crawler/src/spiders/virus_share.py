import logging

import requests

logger = logging.getLogger("GW:gw_scraper")
# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from virus share portal """
import scrapy
from lxml import html as html_xml

from src.spiders.scraper import Scraper
from scrapy.loader import ItemLoader
from src.items import MaliciousFileCrawlerItem

logger = logging.getLogger(__name__)


class VirusShareScraper(Scraper):
    """
        virus share api https://virusshare.com/apiv2/
        hash url https://virusshare.com/hashfiles/unpacked_hashes.md5
        Get the malware url using hashes and api and send it to storage
    """
    name = 'virusshare'
    # Allow duplicate url request (we will be crawling "page 1" twice)
    # custom_settings will only apply these settings in this spider
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, config=None, data=None):
        super(VirusShareScraper, self).__init__()
        self.cfg = config
        self.base_url = self.cfg.get('base_url')
        self.url = self.cfg.get('virusshare_url')
        self.hash_url = self.cfg.get('virusshare_hash_url')
        self.request_mode = "download"
        self.api_key = self.cfg.get('vs_api_key')

    def start_requests(self):
        logger.info(f'Site url : {self.base_url}')
        yield scrapy.Request(url=self.base_url, callback=self.parser)

    def parser(self, response):
        logger.debug("download_files")
        
        hashes = self.scrape_hashes()

        for _hash in hashes:
            url = self.url.format(self.request_mode, self.api_key, _hash)
            html = html_xml.fromstring(url)
            loader = ItemLoader(item=MaliciousFileCrawlerItem())
            loader.add_value('file_urls', url)
            yield loader.load_item()

    def scrape_hashes(self):
        """
        Retrieve all hashes from  VS and save to csv file
        """
        response = VirusShareScraper.get(self.hash_url)

        hashes = []
        response = response.content.split(b'\n')

        for each in response[1:-2]:
            try:
                hashes.append(each.split(b"  ")[1].decode("utf-8"))
            except Exception as error:
                continue
        return hashes

    def get(url):
        headers = {
            "Accept": "text/html, application/xhtml+xml, application/xml",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US, en",
            "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        }
        """
        Fetch url
        """
        try:
            response = requests.get(url, headers=headers)
            return response
        except Exception:
            return False
