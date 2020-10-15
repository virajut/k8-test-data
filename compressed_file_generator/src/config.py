import os
from dotenv import load_dotenv
env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

class Config(object):
    DEBUG = True
    download_path = "/usr/src/app/download/"
    upload_path="/usr/src/app/upload/"

    S3_URL = os.environ["S3_ENDPOINT"]
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY_ID"]
    S3_SECRET_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
    S3_REGION = os.environ["S3_REGION"]
    S3_BUCKET = os.environ["S3_BUCKET"]

    MINIO_URL = os.environ["MINIO_URL"]
    MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
    MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]

    NUM_OF_FILES=int(os.environ["NUM_OF_FILES"])

