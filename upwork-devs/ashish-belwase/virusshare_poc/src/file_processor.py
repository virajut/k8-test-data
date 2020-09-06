from file_service import FileService
from glasswall_service import GlasswallService


class FileProcessor:
    @staticmethod
    def process(file):
        file_info = {}
        FileService.save_file(file)
        FileService.upload_to_s3(file)
        file_info["is_malicious"] = GlasswallService.check_malicious(file)
        return file_info
