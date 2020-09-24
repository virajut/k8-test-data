""" Main class for initializing and running crawlers. """

import os
import sys

from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from scrapyd_api import ScrapydAPI
from src.utils.read_config import ConfigReader

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class DistributedCrawlRunner(object):
    """ Initialize crawler with project settings """

    def __init__(self, *spidercfg):
        self.settings = get_project_settings()  # Scrapy settings
        self.spidercfg = spidercfg
        self.scrapyd = ScrapydAPI(self.settings.get('SCRAPYD_ENDPOINT'))
        self.project_name = self.settings.get('PROJECT_NAME')
        self.extra_settings = {'JOBDIR': self.settings.get('JOB_DIR')}
        print("Initialized ScrapydAPI object: {} "
              "for Project: {} with settings: {}".format(self.scrapyd,
                                                         self.project_name,
                                                         self.extra_settings))

    """ Get all the sites to crawl from config file """

    def get_sites_and_config(self, scrape_site=None):

        if scrape_site is None:
            section = "SCRAPE_SITE"
            try:
                config_obj = ConfigReader(section).read_config()
                sites_arr = config_obj['scrape_sites'].split(',')
                print(sites_arr)
            except KeyError as ke:
                raise CloseSpider(reason="Error while getting site list from config.")

        else:
            sites_arr = scrape_site.split(",")

        site_cfg = {}

        # construct site_cfg dictionary: {site_name: site_cfg}
        for site in sites_arr:
            try:
                cfg = ConfigReader(site.upper()).read_config()
                site_cfg[site] = cfg
            except KeyError as ke:
                raise CloseSpider

        print(site_cfg)
        return site_cfg

    def schedule_job(self, site_arr):

        for site, cfg in site_arr.items():
            """ run crawler for every site and get response list """
            print("Starting to schedule scrapyd process.")
            self.scrapyd.schedule(project=self.settings.get('PROJECT_NAME'),
                                  spider=cfg.get('name'),
                                  settings=self.extra_settings,
                                  config=site)


if __name__ == '__main__':

    scraper = DistributedCrawlRunner()

    """ get site list and corresponding config into a dictionary """
    if len(sys.argv) == 2:
        scrape_site = sys.argv[1]
        site_list = scraper.get_sites_and_config(scrape_site=scrape_site)
    else:
        site_list = scraper.get_sites_and_config()

    scraper.schedule_job(site_list)
