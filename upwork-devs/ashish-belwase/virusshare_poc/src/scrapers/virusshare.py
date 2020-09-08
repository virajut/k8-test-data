import csv
from .base import BaseScraper


class VSScraper(BaseScraper):
    def __init__(self, api_key="", request_mode="download"):
        self.url = "https://virusshare.com/apiv2/{}?apikey={}&hash={}"
        self.hash_url = "https://virusshare.com/hashfiles/unpacked_hashes.md5"
        self.request_mode = request_mode
        self.api_key = api_key

    def scrape_file(self, hash):
        url = self.url.format(self.request_mode, self.api_key, hash)
        response = VSScraper.get(url)
        file_name = response.headers["Content-Disposition"].split("filename=")[1]
        with open(VSScraper.download_path + file_name, "wb") as fp:
            fp.write(response.content)
        return file_name

    def scrape_hashes(self):
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
