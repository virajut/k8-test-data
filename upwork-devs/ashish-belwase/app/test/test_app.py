from unittest.mock import patch
from io import BytesIO
import os

from test import BaseTestCase


class HashResponse:
    content = "  0c3232\n  3208fh32\n  32893293\n  uehi232\n  fij320382"
    status_code = 200


class AppTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(AppTestCase, self).setUp()

    @patch("src.scrapers.virusshare.VSScraper.scrape_file")
    def test_scrape_vs_file(self, mocked_scrape):
        endpoint = "/scrape-vs-file"
        expected = {"file_name": "test_file.png"}
        mocked_scrape.return_value = "test_file.png"

        response = self.client.post(endpoint, json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("api_key and hash required", response.get_json()["error"])

        payload = {
            "api_key": "12332839h98h2309823",
            "hash": "0c02d22721b03f49339e7c89b6dd2cb8",
        }
        response = self.client.post(endpoint, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), expected)

    @patch("src.integrations.virustotal.Virustotal.validate_response")
    def test_check_malicious(self, mocked_resp):
        endpoint = "/check-malicious"
        mocked_resp.return_value = expected = {
                    'json_resp': {
                        'md5': '5058f1af8388633f609cadb75a75dc9d',
                        'permalink': 'https://www.virustotal.com/gui/file/cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8/detection/f-cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8-1599537072',
                        'resource': 'cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8',
                        'response_code': 1,
                        'scan_id': 'cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8-1599537072',
                        'sha1': '3a52ce780950d4d969792a2559cd519d7ee8c727',
                        'sha256': 'cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8',
                        'verbose_msg': 'Scan request successfully queued, come back later for the report'
                        },
                    'status_code': 200
                    }

        response = self.client.post(endpoint, data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("file required", response.get_json()["error"])

        response = self.client.post(
            endpoint,
            content_type="multipart/form-data",
            data={"file": (BytesIO(b"."), "sample.txt")},
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected, response.get_json())

    @patch("src.scrapers.virusshare.VSScraper.get")
    def test_vs(self, mocked_get):
        mocked_get.return_value = HashResponse()
        hash_file = "hashes.csv"
        if os.path.exists(hash_file):
            os.system(f"rm {hash_file}")

        endpoint = "/scrape-vs"
        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 200)

        # check file downloaded
        self.assertTrue(os.path.exists(hash_file))
        with open(hash_file, "r") as f:
            self.assertIn("32893293", f.read())
        os.system(f"rm {hash_file}")
