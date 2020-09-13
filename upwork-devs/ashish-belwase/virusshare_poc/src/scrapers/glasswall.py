import csv
import re
from bs4 import BeautifulSoup
import logging

from src.config import Config
from src.file_service import FileService
from .base import BaseScraper

logger = logging.getLogger("GW:gw_scraper")


class GlasswallScraper(BaseScraper):
    url = Config.glasswall_url

    def __init__(self):
        pass

    @staticmethod
    def download_pdf():
        """
        Download pdf files from glasswall site
        """
        response = BaseScraper.get(GlasswallScraper.url + "/technology")
        if response:
            soup = BeautifulSoup(response.content, "lxml")
            pdfs = soup.findAll("a", href=re.compile(r".*.pdf"))
            logger.info("downloading {} pdfs".format(len(pdfs)))
            for pdf in pdfs:
                url = pdf.get("href")
                try:
                    f = BaseScraper.get_file_from_url(url)
                    FileService.store_files(f)
                except Exception as ex:
                    logger.info("Error saving file {}".format(str(ex)))

    @staticmethod
    def scrape():
        """
        Fetch all files from glasswall
        """
        logger.info("scraping {}".format(GlasswallScraper.url))
        GlasswallScraper.download_pdf()
