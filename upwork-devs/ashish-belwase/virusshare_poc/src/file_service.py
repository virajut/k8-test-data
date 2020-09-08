import os


class FileService:

    UPLOAD_DIR = os.environ.get("STATIC_PATH", "src/static")

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
        path = f"{d}/{file.filename}"
        file.save(path)
        return path
