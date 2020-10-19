import os
import logging
import requests
from minio import Minio
from src.config import Config
from src.utils.s3_client import S3Client

logger = logging.getLogger("GW:s3")


class GovUKFileMigration:
    """ Class to migrate gov_uk files from s3 through the standard k8-test-data file processing
        and upload back the bundled zip with the rebuild data, file meta data, virus-total report
        along with the zipped original file to respective s3 buckets."""

    def __init__(self):
        self.s3 = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
        logger.info("GovUKFileMigration::__init__ Creating s3 client object: %s" % self.s3)
        self.download_dir = Config.LOCAL_REPO_PATH
        self.n_files_to_fetch = float('inf')
        self.file_obj = self.s3.download_subdirectory_files(Config.S3_BUCKET, Config.S3_SUB_FOLDER_PREFIX,
                                                            self.n_files_to_fetch,
                                                            file_download_path=self.download_dir)

    def get_file(self):

        # download files from s3 bucket using s3client generator method
        try:
            file_obj = next(self.file_obj)
            logger.info("GovUKFileMigration::get_file "
                        "Downloaded file {} from s3.".format(file_obj))
        except Exception as e:
            logger.info("GovUKFileMigration::get_file Got error {} "
                        "while downloading files from {}.".format(e, Config.S3_BUCKET))
            return -1

        return file_obj

    @staticmethod
    def get_bucket_name(path):

        # extract file stats and return bucket name
        extension = path.split("/")[-1].split('.')[-1]
        if extension:
            bucket_name = extension.lower()
        else:
            bucket_name = 'hash'
        minio_path = path.split("/")[-1]
        file_stat = os.stat(path)

        return bucket_name

    def preprocess_files(self, file):

        # 1. extract meta data of the file
        bucket_name = GovUKFileMigration.get_bucket_name(file)
        file_name = file.split('/')[-1]

        logger.info("GovUKFileMigration::preprocess_files Iterating file: %s |"
                    " Bucket Name: %s | Filename: %s" % (file, bucket_name, file_name))

        try:
            # 2. upload the file to minio before passing it to processor.
            GovUKFileMigration.upload_to_minio(bucket_name=bucket_name, file_path=file, file_name=file_name)
        except Exception as e:
            logger.info("GovUKFileMigration::preprocess_files Got error {} "
                        "while uploading to minio.".format(e))
            raise e

        # 3. pass received file to file processor
        processor_response = GovUKFileMigration.process_file(file=file, bucket_name=bucket_name)
        logger.info("GovUKFileMigration::preprocess_files File processor response: %s for "
                    "file %s and bucket name %s" % (processor_response, file, bucket_name))

    @staticmethod
    def upload_to_minio(bucket_name, file_name, file_path):

        logger.info("GovUKFileMigration::upload_to_minio Uploading %s present at %s "
                    "to minio bucket %s" % (file_name, file_path, bucket_name))
        _client = Minio(endpoint=Config.MINIO_ENDPOINT,
                        access_key=Config.MINIO_ACCESS_KEY,
                        secret_key=Config.MINIO_SECRET_KEY,
                        secure=False)

        if not _client.bucket_exists(bucket_name):
            _client.make_bucket(bucket_name=bucket_name)
            logger.info("GovUKFileMigration::upload_to_minio created bucket %s with "
                        "client object %s" % (bucket_name, _client))
        try:
            _client.fput_object(bucket_name=bucket_name,
                                object_name=file_name,
                                file_path=file_path)
            logger.info(f"GovUKFileMigration::upload_to_minio Uploaded file {file_name}")
        except Exception as e:
            logger.error("GovUKFileMigration::upload_to_minio Got error while uploaing to minio %s" % e)
            raise Exception(e)

    @staticmethod
    def process_file(file, bucket_name):

        payload = {
            "file": file.split('/')[-1],
            "bucket": bucket_name
        }

        try:
            file_processor_api = os.environ.get('file_processor_api', None)
            fp_response = requests.post(file_processor_api, json=payload)
            logger.info("GovUKFileMigration::process_file Got response %s while processing file"
                        "with payload %s" % (fp_response, payload))

        except Exception as e:
            logger.error("GovUKFileMigration::process_file Got error %s while processing file"
                         "with payload %s" % (payload, e))
            raise e

        return fp_response.status_code


if __name__ == '__main__':

    # create compression obj
    migration_obj = GovUKFileMigration()

    # fetch files
    s3_file = float('inf')  # this will be used to stop fetching file from the file download generator
    while s3_file != -1:
        # keep fetching files from file generator unless iterator is exhausted: -1
        s3_file = migration_obj.get_file()
        logger.info("GovUKFileMigration::__main__ Files from gov-uk bucket: {}".format(s3_file))

        # send files for processing through the k8-test-data standard processing
        if s3_file != -1:
            migration_obj.preprocess_files(s3_file)







