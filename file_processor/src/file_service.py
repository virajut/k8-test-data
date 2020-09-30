import os
from os.path import basename
import zipfile
from src.services import MinioService


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
    def prepare_zip(zip_filename, file, zip_path):

        zip_filename = f"{zip_path}/{zip_filename}.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipObj:
            for folderName, subfolders, filenames in os.walk(zip_path):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))
        return zip_filename
