import requests
import os


class BaseScraper:

    headers = {
        "Accept": "text/html, application/xhtml+xml, application/xml",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US, en",
        "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    }
    download_path = os.environ.get("STATIC_PATH", "src/static")
    unzip_path = download_path + "/zp"

    @staticmethod
    def get(url):
        try:
            response = requests.get(url, headers=BaseScraper.headers)
            return response
        except Exception:
            return False
