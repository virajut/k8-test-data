import os
import uuid
import zipfile
from src.minio_service import Minio
from src.constants import download_path


class FileService:

    UPLOAD_DIR = os.environ.get("STATIC_PATH", "src/static")

    @staticmethod
    def zip_files(files):
        fname = download_path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        for f in files:
            arcname = f.rsplit("/", 1)[-1]
            zipObj.write(f, arcname=arcname)
        zipObj.close()
        return fname

    @staticmethod
    def unzip_files(f):
        with zipfile.ZipFile(f, "r") as zp:
            zp.extractall(download_path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8"))

    @staticmethod
    def get_local_files():
        files = []
        for f in os.listdir(download_path):
            files.append(download_path + "/" + f)
        return files

    @staticmethod
    def save_file(file):
        d = FileService.UPLOAD_DIR
        if not os.path.exists(d):
            os.makedirs(d)
        path = f"{d}/{file.filename}"
        file.save(path)
        return path

    @staticmethod
    def save_to_minio(file_path):
        file_name = file_path.split("/")[-1]
        file_exention = file_path.split(".")[-1]
        url = os.getenv("MINIO_URL")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        minio = Minio(url, access_key, secret_key)
        return minio.upload_to_minio(file_path, file_exention, file_name)

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
            zipped_file = FileService.zip_files(files)
        return zipped_file
