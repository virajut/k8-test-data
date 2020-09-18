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
    def zip_files(files, key=None):
        """
        Compress :files to zip
        """
        path = download_path
        if key:
            path = path + "/" + key
        fname = download_path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        for file in files:
            arcname = file.rsplit("/", 1)[-1]
            zipObj.write(file, arcname=arcname)
        zipObj.close()
        return fname

    @staticmethod
    def unzip_files(file, key=None):
        """
        Unzip :file to local path
        """
        with zipfile.ZipFile(file, "r") as zp:
            path = download_path
            if key:
                path = download_path + "/" + key
            zp.extractall(path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8"))

    @staticmethod
    def get_local_files(key=None):
        """
        Return all files from local storage folder
        """
        files = []
        path = download_path
        if key:
            path = path + "/" + key
        for file in os.listdir(path):
            files.append(path + "/" + file)
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
    def store_file(file_path):
        """
        Put file to Minio
        """
        file_meta = FileService.get_file_meta(file_path)
        if not file_meta:
            logger.info(f"Unable to get file meta for {file_path}")

        storage = FileService.get_storage()
        return storage.upload(file_path, file_meta["extension"], file_meta["name"])

    @staticmethod
    def store_vs_files(files, ext):
        """
        Put VS files to Minio
        """
        storage = FileService.get_storage()
        for f in files:
            filename = f.rsplit("/", 1)[-1]
            storage.upload(f, ext, filename)

    @staticmethod
    def process_zip(file):
        """
        Takes zip file, unzip it , extract meta and send to storage
        """
        from src.scrapers import VSScraper

        FileService.unzip_files(file, file.filename)
        parent_path = download_path + "/" + file.filename
        for zipfilename in os.listdir(parent_path):
            # To do : run these on each K8-pod

            ext = VSScraper.get_zip_extension(zipfilename)
            if not ext:
                # skip file without extension
                continue

            FileService.unzip_files(parent_path + "/" + zipfilename, zipfilename)
            files = FileService.get_local_files(zipfilename)
            FileService.store_vs_files(files, ext)
