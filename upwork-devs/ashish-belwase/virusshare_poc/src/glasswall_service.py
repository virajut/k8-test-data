import os
from src.integrations import Virustotal


class GlasswallService:
    @staticmethod
    def check_malicious(file_path):
        vt = Virustotal(os.environ.get("virustotal_key"))
        resp = vt.file_scan(file_path)
        return resp
