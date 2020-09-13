import os
import uuid
import zipfile
import logging
from src.minio_service import Minio
from src.constants import download_path

logger = logging.getLogger("GW:file_service")


class FileService:

    UPLOAD_DIR = os.environ.get("STATIC_PATH", "src/static")

    @staticmethod
    def get_file_meta(file_path):
        meta = {}
        try:
            meta["name"] = file_path.split("/")[-1]
            meta["extension"] = file_path.split(".")[-1]
        except Exception:
            return None
        else:
            return meta

    @staticmethod
    def zip_files(files):
        """
        Compress :files to zip
        """
        fname = download_path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        for file in files:
            arcname = file.rsplit("/", 1)[-1]
            zipObj.write(file, arcname=arcname)
        zipObj.close()
        return fname

    @staticmethod
    def unzip_files(file):
        """
        Unzip :file to local path
        """
        with zipfile.ZipFile(file, "r") as zp:
            zp.extractall(download_path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8"))

    @staticmethod
    def get_local_files():
        """
        Return all files from local storage folder
        """
        files = []
        for file in os.listdir(download_path):
            files.append(download_path + "/" + file)
        return files

    @staticmethod
    def save_file(file):
        """
        Save file to local storage folder
        """
        path = FileService.UPLOAD_DIR
        if not os.path.exists(path):
            os.makedirs(path)
        path = f"{path}/{file.filename}"
        file.save(path)
        return path

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
    def store_files(file_path):
        """
        Put file to Minio
        """
        file_meta = FileService.get_file_meta(file_path)
        if not file_meta:
            logger.info(f"Unable to get file meta for {file_path}")

        storage = FileService.get_storage()
        return storage.upload(file_path, file_meta["extension"], file_meta["name"])

    @staticmethod
    def get_files(file_type, num_files):
        """
        Downloads given number of files from a minio bucket of give file_type
        """
        minio = FileService.get_storage()
        files = minio.download_files(file_type, num_files)
        zipped_file = FileService.zip_files(files) if files else None
        return zipped_file
