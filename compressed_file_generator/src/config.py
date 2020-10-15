import os

from dotenv import load_dotenv

env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


class Config(object):
    DEBUG = True
    download_path = "download/"
    upload_path = "upload/"

    S3_URL = os.environ["S3_ENDPOINT"]
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY_ID"]
    S3_SECRET_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
    S3_REGION = os.environ["S3_REGION"]

    SOURCE_S3_BUCKET = os.environ["SOURCE_S3_BUCKET"]
    TARGET_S3_BUCKET = os.environ["TARGET_S3_BUCKET"]

    NUM_OF_FILES = int(os.environ["NUM_OF_FILES"])

    Allowed_types = ["doc", "dot", "xls", "xlt", "xlm", "ppt", "pot", "pps", "docx", "dotz", "docm", "dotm", "xlsx",
                     "xltx", "xlsm", "xltm", "pptx", "potx", "ppsx", "pptm", "potm", "ppsm", "pdf", "jpeg", "jpg",
                     "jpe",
                     "png", "gif"]
