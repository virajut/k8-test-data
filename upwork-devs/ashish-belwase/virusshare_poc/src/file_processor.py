from src.file_service import FileService
from src.glasswall_service import GlasswallService


class FileProcessor:
    @staticmethod
    def process(file):
        f = FileService.save_file(file)
        FileService.upload_to_s3(file)
        file_info = GlasswallService.check_malicious(f)
        return file_info
