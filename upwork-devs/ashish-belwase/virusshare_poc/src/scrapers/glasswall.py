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
        response = BaseScraper.get(GlasswallScraper.url + "/technology")
        if response:
            soup = BeautifulSoup(response.content, "lxml")
            pdfs = soup.findAll("a", href=re.compile(r".*.pdf"))
            logger.info("downloading {} pdfs".format(len(pdfs)))
            for pdf in pdfs:
                url = pdf.get("href")
                f = BaseScraper.get_file_from_url(url)
                FileService.save_to_minio(f)

    @staticmethod
    def scrape():
        """
        fetch all files from glasswall
        """
        logger.info("scraping {}".format(GlasswallScraper.url))
        GlasswallScraper.download_pdf()
