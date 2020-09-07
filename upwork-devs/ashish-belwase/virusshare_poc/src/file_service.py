import os


class FileService:

    UPLOAD_DIR = "/usr/src/app/src/static"

    @staticmethod
    def upload_to_s3(file):
        """
        to implement later after getting a demo credentials
        """
        pass

    @staticmethod
    def save_file(file):
        d = FileService.UPLOAD_DIR
        if not os.path.exists(d):
            os.makedirs(d)
        file.save(f"{d}/{file.filename}")
