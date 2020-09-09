import zipfile
import os

from src.file_service import FileService
from src.glasswall_service import GlasswallService
from src.scrapers import VSScraper


class FileProcessor:
    @staticmethod
    def get_valid_zip_files(f):
        files_to_check = []
        with zipfile.ZipFile(f, "r") as zp:
            zp.extractall(
                VSScraper.unzip_path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8")
            )
            for f in os.listdir(VSScraper.unzip_path):
                if GlasswallService.is_valid_type(f):
                    files_to_check.append(VSScraper.unzip_path + "/" + f)
        return files_to_check

    @staticmethod
    def process(file):
        f = FileService.save_file(file)
        FileService.upload_to_s3(file)
        file_info = GlasswallService.check_malicious(f)
        return file_info

    @staticmethod
    def process_vs_hash(hashes):
        infos = []
        for h in hashes:
            vs = VSScraper(os.environ["vs_api_key"])
            f = vs.scrape_file(h.strip())
            files_to_check = []
            if zipfile.is_zipfile(f):
                files_to_check = FileProcessor.get_valid_zip_files(f)
            else:
                files_to_check = [f]
            break

        for f in files_to_check:
            file_info = GlasswallService.check_malicious(f)
            infos.append(file_info)

        return infos
