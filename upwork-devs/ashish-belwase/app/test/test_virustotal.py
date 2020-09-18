from unittest.mock import patch
import os

from test import BaseTestCase
from src.integrations import Virustotal

FilePostResponse = {"status_code": 200, "json_resp": {"response_code": 1}}


class VirusTotalTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(VirusTotalTestCase, self).setUp()
        self.vt = Virustotal("")

    @patch("src.integrations.virustotal.Virustotal.make_request")
    def test_file_scan(self, mocked_post):

        f = "test.txt"
        mocked_post.return_value = FilePostResponse

        if not os.path.exists(f):
            os.system(f"touch {f}")
        resp = self.vt.file_scan(f)
        self.assertEqual(resp["status_code"], 200)
        self.assertEqual(resp["json_resp"]["response_code"], 1)

    @patch("src.integrations.virustotal.Virustotal.make_request")
    def test_url_report(self, mocked_post):
        mocked_post.return_value = FilePostResponse
        resp = self.vt.url_report(["malicious.info"], scan=1)
        self.assertEqual(resp["status_code"], 200)
        self.assertEqual(resp["json_resp"]["response_code"], 1)

    @patch("src.integrations.virustotal.Virustotal.make_request")
    def test_ipaddress_report(self, mocked_post):
        mocked_post.return_value = FilePostResponse
        resp = self.vt.url_report(["54.90.23.1"], scan=1)
        self.assertEqual(resp["status_code"], 200)
        self.assertEqual(resp["json_resp"]["response_code"], 1)

    @patch("src.integrations.virustotal.Virustotal.make_request")
    def test_domain_report(self, mocked_post):
        mocked_post.return_value = FilePostResponse
        resp = self.vt.url_report(["abc.info"], scan=1)
        self.assertEqual(resp["status_code"], 200)
        self.assertEqual(resp["json_resp"]["response_code"], 1)
