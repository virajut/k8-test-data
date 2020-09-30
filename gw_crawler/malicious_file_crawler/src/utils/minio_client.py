import logging
import os
import sys

import requests

sys.path.append(os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ))
)

logger = logging.getLogger("GW:minio")


class MinioClient:
    """
            It calls storage adapter to get minio client
    """
    server_base_url = 'http://localhost:50052/'

    @staticmethod
    def upload_file(bucket_name, minio_path, file, server_base_url=server_base_url):
        try:
            data = {'bucket_name': bucket_name,
                    "minio_path": minio_path,
                    "file": file, }
            return requests.post(server_base_url + "upload", json=data)
        except Exception as e:
            logger.error(f'MinioClient : upload_file : {e} ')
