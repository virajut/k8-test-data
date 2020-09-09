import os


class FileService:

    UPLOAD_DIR = os.environ.get("STATIC_PATH", "src/static")

    @staticmethod
    def save_file(file):
        # To Do :  to be replaced by minio file save service
        d = FileService.UPLOAD_DIR
        if not os.path.exists(d):
            os.makedirs(d)
        path = f"{d}/{file.filename}"
        file.save(path)
        return path
