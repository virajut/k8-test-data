import os
from src.integrations import Virustotal


class GlasswallService:

    Allowed_Types = [".doc", ".pdf", ".ppt"]

    @staticmethod
    def check_malicious(file_path):
        """
        Query VirusTotal api to check if file is malicious
        """
        vt = Virustotal(os.environ.get("virustotal_key"))
        resp = vt.file_scan(file_path)
        return resp

    @staticmethod
    def is_valid_type(file_name):
        """ 
        Check if file is valid , skip for now
        """
        return True
        ext = file_name.rsplit(".", 1)[-1]
        if ext in GlasswallService.Allowed_Types:
            return True
        return False
