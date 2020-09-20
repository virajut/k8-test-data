import os
import uuid
import zipfile
from src.minio_service import Minio
from src.config import Config


class FileService:
    @staticmethod
    def zip_files(files, key=None):
        """
        Compress :files to zip
        """
        path = Config.download_path
        if key:
            path = path + "/" + key
        fname = path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        for file in files:
            arcname = file.rsplit("/", 1)[-1]
            zipObj.write(file, arcname=arcname)
        zipObj.close()
        return fname

    @staticmethod
    def get_storage():
        """
        Get storage platform which currently is Minio
        """
        url = os.getenv("MINIO_URL")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        storage = Minio(url, access_key, secret_key)
        return storage

    @staticmethod
    def get_files(file_type, num_files):
        """
        Downloads given number of files from a minio bucket of give file_type
        """
        minio = FileService.get_storage()
        files = minio.download_files(file_type, num_files)
        zipped_file = FileService.zip_files(files) if files else None
        return zipped_file
