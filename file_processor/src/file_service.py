import os
import zipfile


class FileService:
    @staticmethod
    def unzip(file_path, extract_path, password=None):
        with zipfile.ZipFile(file_path, "r") as zp:
            params = {
                "path": extract_path,
            }
            if password:
                params["pwd"] = bytes(os.environ["vs_zip_pwd"], "utf-8")
            zp.extractall(**params)

    @staticmethod
    def prepare_zip(file):
        pass

    @staticmethod
    def upload(file):
        pass
