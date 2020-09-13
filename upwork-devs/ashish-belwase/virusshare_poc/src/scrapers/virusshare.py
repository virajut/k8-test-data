import csv
import logging

from src.file_service import FileService
from src.config import Config
from .base import BaseScraper

logger = logging.getLogger("GW:gw_scraper")


class VSScraper(BaseScraper):
    def __init__(self, vs_api_key="", request_mode="download"):
        self.url = Config.virusshare_url
        self.hash_url = Config.virusshare_hash_url
        self.request_mode = request_mode
        self.api_key = vs_api_key

    def scrape_file(self, hash):
        """
        Get VS file from hash and store to local path
        """
        url = self.url.format(self.request_mode, self.api_key, hash)
        response = VSScraper.get(url)
        file_name = (
            VSScraper.download_path
            + response.headers["Content-Disposition"].split("filename=")[1]
        )
        with open(file_name, "wb") as fp:
            fp.write(response.content)
        return file_name

    def scrape_hashes(self):
        """
        Retrieve all hashes from  VS and save to csv file
        """
        response = VSScraper.get(self.hash_url)
        hashes = []
        response = response.content.split("\n")
        for each in response[1:-2]:
            try:
                hashes.append(each.split("  ")[1])
            except Exception as error:
                continue
        with open("hashes.csv", "w") as file:
            writer = csv.writer(file, dialect="excel")
            for each in hashes:
                writer.writerow([each])

    def get_demo_hashes(self):
        """
        For demo return static hashes
        """
        return [
            "0002d20a7423518b7f371302014076c9",
            "00034b48dddb5b717481935c292ad2ef",
            "000432d85e14ea16d2ce3f23b9c11d8e",
            "00070feb80aeb037fdeef4fc1ccf6a4a",
            "0007d7c9debd4fb9ccc2f2fa1e91a4ef",
            "0008501ca611695123adde105429c486",
            "000a6d40eee7814b8243a0d8c19f94c3",
            "000aae411d6697e6afb3dffaf194682d",
            "000be57dc7d0013ae5c1cd9cc53c58a8",
            "0015760015829eded58ccc8727fe466f",
        ]

    def process_hashes(self, hashes):
        """
        Get file from each hashes and save to storage
        """
        for _hash in hashes:
            try:
                f = self.scrape_file(_hash.strip())
                FileService.store_files(f)
            except Exception:
                continue

    def scrape(self):
        """
        Get all hashes and save to storage
        """
        logger.info("scraping {}".format(self.url))
        hashes = self.get_demo_hashes()
        self.process_hashes(hashes)
