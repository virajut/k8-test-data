# -*- coding: utf-8 -*-
""" Scraper class for getting vehicles from carwave portal """
import scrapy
import wget
from scrapy.loader import ItemLoader
from malicious_file_crawler.src.items import MaliciousFileCrawlerItem
import json
import requests
from malicious_file_crawler.src.spiders.scraper import Scraper
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1200x600')
# options.add_experimental_option("prefs", {
#   "download.default_directory": "D:\\malicious_files\\",
# })
prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
options.add_experimental_option("prefs", prefs)
# remoteWebDriverUrl = "http://192.168.99.100:4444/wd/hub"


class GlasswallScraper(Scraper):
    name = 'glasswall_spider'
    # allowed_domains = ['carwave.com']

    # Allow duplicate url request (we will be crawling "page 1" twice)
    # custom_settings will only apply these settings in this spider
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, config=None, data=None):
        super(GlasswallScraper, self).__init__()
        self.cfg = config
        self.login_url = self.cfg.get('login_url')
        self.start_urls = [self.login_url]
        self.file_page_url = self.cfg.get("file_page_url")
        # self.driver = webdriver.Remote(remoteWebDriverUrl,
        #                                desired_capabilities=DesiredCapabilities.CHROME)

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """

        print("start requests:", self.start_urls)
        for url in self.start_urls:
            yield scrapy.Request(url,
                                 callback=self.navigate_to)

    def navigate_to(self, response):
        yield scrapy.Request(self.file_page_url,
                             callback=self.download_files)

    def download_files(self, response):
        print(response, response.body)
        # get download all file link
        download_all_link = response.xpath("//li[@id='download']/a/@href").get()

        loader = ItemLoader(item=MaliciousFileCrawlerItem())
        loader.add_value('file_urls', download_all_link)
        yield loader.load_item()
