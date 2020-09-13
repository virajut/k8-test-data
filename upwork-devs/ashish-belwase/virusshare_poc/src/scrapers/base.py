import requests
import os
import uuid
import urllib.request

from src.constants import download_path


class BaseScraper:

    headers = {
        "Accept": "text/html, application/xhtml+xml, application/xml",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US, en",
        "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    }

    @staticmethod
    def get(url):
        """
        Fetch url
        """
        try:
            response = requests.get(url, headers=BaseScraper.headers)
            return response
        except Exception:
            return False

    @staticmethod
    def get_file_from_url(url):
        """
        Fetch url as file
        """
        ext = url.split(".")[-1]
        path = download_path + "/" + str(uuid.uuid4()) + "." + ext
        urllib.request.urlretrieve(url, path)
        return path
