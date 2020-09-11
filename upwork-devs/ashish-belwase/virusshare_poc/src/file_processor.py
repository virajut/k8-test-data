import zipfile
import os
import uuid

from src.file_service import FileService
from src.glasswall_service import GlasswallService
from src.scrapers import VSScraper
from src.minio_service import Minio


class FileProcessor:
    @staticmethod
    def zip_file(f):
        fname = VSScraper.download_path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        arcname = f.rsplit("/", 1)[-1]
        zipObj.write(f, arcname=arcname)
        zipObj.close()
        return fname

    @staticmethod
    def zip_files(files):
        fname = VSScraper.download_path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        for f in files:
            arcname = f.rsplit("/", 1)[-1]
            zipObj.write(f, arcname=arcname)
        zipObj.close()
        return fname

    @staticmethod
    def unzip_files(f):
        with zipfile.ZipFile(f, "r") as zp:
            zp.extractall(
                VSScraper.download_path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8")
            )

    @staticmethod
    def get_local_files():
        files = []
        for f in os.listdir(VSScraper.download_path):
            if GlasswallService.is_valid_type(f):
                files.append(VSScraper.download_path + "/" + f)
        return files

    @staticmethod
    def process(file):
        f = FileService.save_to_minio(file)
        file_info = GlasswallService.check_malicious(f)
        return file_info

    @staticmethod
    def process_vs_hash(hashes):
        infos = []
        for h in hashes:
            vs = VSScraper(os.environ["vs_api_key"])
            f = vs.scrape_file(h.strip())
            if not zipfile.is_zipfile(f):
                f = FileProcessor.zip_file(f)

            FileService.save_to_minio(f)
            break

        # skipping this for now
        return infos
        files_to_check = FileProcessor.get_local_files()
        for f in files_to_check:
            file_info = GlasswallService.check_malicious(f)
            # if not malicious, remove it
            if not file_info:
                os.remove(f)

            infos.append(file_info)

        return infos

    @staticmethod
    def get_files(file_type, num_files):
        "Downloads given number of files from a minio bucket of specific file types"
        url = os.getenv("MINIO_URL")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        minio = Minio(url, access_key, secret_key)
        files = minio.download_files(file_type, num_files)
        zipped_file = None
        if files:
            zipped_file = FileProcessor.zip_files(files)
        return zipped_file
