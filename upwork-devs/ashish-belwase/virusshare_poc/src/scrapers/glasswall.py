import csv
import re
from bs4 import BeautifulSoup
from .base import BaseScraper
from src.file_service import FileService


class GlasswallScraper(BaseScraper):
    url = "https://glasswallsolutions.com"

    def __init__(self):
        pass

    @staticmethod
    def download_pdf():
        response = BaseScraper.get(GlasswallScraper.url + "/technology")
        if response:
            soup = BeautifulSoup(response.content, "lxml")
            pdfs = soup.findAll("a", href=re.compile(r".*.pdf"))
            print("downloading {} pdfs".format(len(pdfs)))
            for pdf in pdfs:
                url = pdf.get("href")
                f = BaseScraper.get_file_from_url(url)
                FileService.save_to_minio(f)
